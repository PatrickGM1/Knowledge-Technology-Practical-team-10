"""Inference engine for applying knowledge base rules to domain objects"""

from typing import List, Dict, Any, Optional, Callable
import yaml
import json
from pathlib import Path


class Rule:
    """Represents a single inference rule"""
    
    def __init__(self, rule_dict: Dict[str, Any]):
        self.id = rule_dict.get('id', '')
        self.name = rule_dict.get('name', '')
        self.description = rule_dict.get('description', '')
        self.priority = rule_dict.get('priority', 0)
        self.conditions = rule_dict.get('conditions', [])
        self.action = rule_dict.get('action', {})
        self.category = rule_dict.get('category', 'general')
    
    def __repr__(self):
        return f"Rule(id='{self.id}', name='{self.name}', priority={self.priority})"


class InferenceEngine:
    """Applies rules from knowledge base to domain objects"""
    
    def __init__(self, kb_path: Optional[str] = None):
        self.rules: List[Rule] = []
        self.facts: Dict[str, Any] = {}
        
        if kb_path:
            self.load_knowledge_base(kb_path)
    
    def load_knowledge_base(self, kb_path: str):
        """Load rules from knowledge base file"""
        path = Path(kb_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Knowledge base file not found: {kb_path}")
        
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                kb_data = yaml.safe_load(f)
            elif path.suffix == '.json':
                kb_data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
        
        # Load rules
        for rule_data in kb_data.get('rules', []):
            rule = Rule(rule_data)
            self.rules.append(rule)
        
        # Sort rules by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def add_fact(self, key: str, value: Any):
        """Add a fact to the working memory"""
        self.facts[key] = value
    
    def get_fact(self, key: str) -> Any:
        """Retrieve a fact from working memory"""
        return self.facts.get(key)
    
    def clear_facts(self):
        """Clear all facts from working memory"""
        self.facts.clear()
    
    def evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single condition"""
        cond_type = condition.get('type', 'attribute_equals')
        obj_name = condition.get('object', 'recipe')
        attribute = condition.get('attribute', '')
        value = condition.get('value')
        operator = condition.get('operator', '==')
        
        # Get the object from context
        obj = context.get(obj_name)
        if obj is None:
            return False
        
        # Get attribute value
        if '.' in attribute:
            # Nested attribute (e.g., 'nutritional_info.calories')
            parts = attribute.split('.')
            attr_value = obj
            for part in parts:
                if hasattr(attr_value, part):
                    attr_value = getattr(attr_value, part)
                else:
                    return False
        else:
            if not hasattr(obj, attribute):
                return False
            attr_value = getattr(obj, attribute)
        
        # Evaluate based on operator
        if operator == '==':
            return attr_value == value
        elif operator == '!=':
            return attr_value != value
        elif operator == '>':
            return attr_value > value
        elif operator == '<':
            return attr_value < value
        elif operator == '>=':
            return attr_value >= value
        elif operator == '<=':
            return attr_value <= value
        elif operator == 'in':
            return attr_value in value if isinstance(value, (list, tuple)) else False
        elif operator == 'not_in':
            return attr_value not in value if isinstance(value, (list, tuple)) else True
        elif operator == 'contains':
            return value in attr_value if hasattr(attr_value, '__contains__') else False
        elif operator == 'method_call':
            # Call a method on the object
            method_name = condition.get('method')
            args = condition.get('args', [])
            if hasattr(obj, method_name):
                method = getattr(obj, method_name)
                # Resolve arguments from context
                resolved_args = []
                for arg in args:
                    if isinstance(arg, str) and arg in context:
                        # Argument refers to an attribute in context
                        resolved_args.append(context[arg])
                    elif isinstance(arg, str):
                        # Try to get attribute from recipe
                        if 'recipe' in context and hasattr(context['recipe'], arg):
                            resolved_args.append(getattr(context['recipe'], arg))
                        else:
                            resolved_args.append(arg)
                    else:
                        resolved_args.append(arg)
                return method(*resolved_args)
            return False
        elif operator == 'not_method_call':
            # Call a method and return the opposite (for negative conditions)
            method_name = condition.get('method')
            args = condition.get('args', [])
            if hasattr(obj, method_name):
                method = getattr(obj, method_name)
                # Resolve arguments from context
                resolved_args = []
                for arg in args:
                    if isinstance(arg, str) and arg in context:
                        resolved_args.append(context[arg])
                    elif isinstance(arg, str):
                        if 'recipe' in context and hasattr(context['recipe'], arg):
                            resolved_args.append(getattr(context['recipe'], arg))
                        else:
                            resolved_args.append(arg)
                    else:
                        resolved_args.append(arg)
                return not method(*resolved_args)
            return True  # If method doesn't exist, assume condition is met for filtering
        
        return False
    
    def evaluate_conditions(self, conditions: List[Dict[str, Any]], context: Dict[str, Any]) -> bool:
        """Evaluate all conditions for a rule"""
        if not conditions:
            return True
        
        logic = conditions[0].get('logic', 'and') if isinstance(conditions[0], dict) else 'and'
        
        if logic == 'and':
            return all(self.evaluate_condition(cond, context) for cond in conditions)
        elif logic == 'or':
            return any(self.evaluate_condition(cond, context) for cond in conditions)
        
        return True
    
    def execute_action(self, action: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute the action specified by a rule"""
        action_type = action.get('type', 'filter')
        
        if action_type == 'filter':
            return {
                'action': 'filter',
                'result': action.get('result', False),
                'reason': action.get('reason', ''),
                'rule_id': action.get('rule_id', '')
            }
        elif action_type == 'score':
            return {
                'action': 'score',
                'score_delta': action.get('score_delta', 0),
                'reason': action.get('reason', '')
            }
        elif action_type == 'substitute':
            return {
                'action': 'substitute',
                'substitutions': action.get('substitutions', {}),
                'reason': action.get('reason', '')
            }
        elif action_type == 'recommend':
            return {
                'action': 'recommend',
                'confidence': action.get('confidence', 1.0),
                'reason': action.get('reason', '')
            }
        
        return None
    
    def apply_rules(self, context: Dict[str, Any], category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Apply all rules to the context"""
        results = []
        
        for rule in self.rules:
            # Skip if category doesn't match
            if category and rule.category != category:
                continue
            
            # Evaluate conditions
            if self.evaluate_conditions(rule.conditions, context):
                # Execute action
                result = self.execute_action(rule.action, context)
                if result:
                    result['rule_name'] = rule.name
                    result['rule_id'] = rule.id
                    results.append(result)
        
        return results
    
    def filter_recipes(self, recipes: List[Any], user: Any) -> List[tuple]:
        """Filter recipes based on user preferences using rules"""
        filtered_recipes = []
        
        for recipe in recipes:
            context = {'user': user, 'recipe': recipe}
            
            # Apply filtering rules
            results = self.apply_rules(context, category='filtering')
            
            # Check if recipe should be filtered out
            should_filter = False
            filter_reasons = []
            
            for result in results:
                if result['action'] == 'filter' and not result['result']:
                    should_filter = True
                    filter_reasons.append(result['reason'])
            
            if should_filter:
                continue
            
            # Apply scoring rules
            score = 0
            score_reasons = []
            
            scoring_results = self.apply_rules(context, category='scoring')
            for result in scoring_results:
                if result['action'] == 'score':
                    score += result['score_delta']
                    score_reasons.append(result['reason'])
            
            filtered_recipes.append((recipe, score, score_reasons))
        
        # Sort by score (highest first)
        filtered_recipes.sort(key=lambda x: x[1], reverse=True)
        
        return filtered_recipes
    
    def get_substitutions(self, recipe: Any, user: Any) -> Dict[str, List[str]]:
        """Get ingredient and cooking method substitutions for a recipe"""
        context = {'user': user, 'recipe': recipe}
        results = self.apply_rules(context, category='substitution')
        
        substitutions = {
            'ingredients': {},
            'cooking_methods': {},
            'equipment': {}
        }
        
        for result in results:
            if result['action'] == 'substitute':
                subs = result.get('substitutions', {})
                for key, value in subs.items():
                    if key == 'ingredient':
                        substitutions['ingredients'].update(value)
                    elif key == 'cooking_method':
                        substitutions['cooking_methods'].update(value)
                    elif key == 'equipment':
                        substitutions['equipment'].update(value)
        
        return substitutions
