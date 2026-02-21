"""Forward-chaining inference engine for recipe recommendation"""

from typing import List, Dict, Any, Optional, Set
import yaml
import json
from pathlib import Path
from .rule import Rule


class InferenceEngine:
    """Applies rules to domain objects using forward-chaining inference"""
    
    def __init__(self, kb_path: Optional[str] = None):
        self.rules: List[Rule] = []
        self.working_memory: Set[str] = set()  # Asserted facts
        self.recipe_facts: Dict[str, Dict[str, Any]] = {}  # Per-recipe facts
        self.fired_rules: List[str] = []
        self.inference_log: List[Dict[str, Any]] = []  # Track reasoning

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
        
        for rule_data in kb_data.get('rules', []):
            rule = Rule(
                id=rule_data.get('id', ''),
                name=rule_data.get('name', ''),
                description=rule_data.get('description', ''),
                priority=rule_data.get('priority', 0),
                conditions=rule_data.get('conditions', []),
                action=rule_data.get('action', {}),
                category=rule_data.get('category', 'general')
            )
            self.rules.append(rule)
        
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        
    def assert_fact(self, fact: str):
        """Assert a new fact into working memory (forward-chaining)"""
        if fact not in self.working_memory:
            self.working_memory.add(fact)
            return True
        return False
    
    def has_fact(self, fact: str) -> bool:
        """Check if a fact exists in working memory"""
        return fact in self.working_memory
    
    def get_recipe_fact(self, recipe_id: str, fact_name: str) -> Any:
        """Get a specific fact about a recipe"""
        return self.recipe_facts.get(recipe_id, {}).get(fact_name)
    
    def set_recipe_fact(self, recipe_id: str, fact_name: str, value: Any) -> bool:
        """Set a fact about a recipe (returns True if changed)"""
        if recipe_id not in self.recipe_facts:
            self.recipe_facts[recipe_id] = {}
        
        old_value = self.recipe_facts[recipe_id].get(fact_name)
        if old_value != value:
            self.recipe_facts[recipe_id][fact_name] = value
            return True
        return False
    
    def clear_working_memory(self):
        """Clear all inferred facts"""
        self.working_memory.clear()
        self.recipe_facts.clear()
        self.fired_rules.clear()
        self.inference_log.clear()
    
    def evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single condition (checks facts and object attributes)"""
        cond_type = condition.get('type', 'attribute')
        
        # Check if it's a fact-based condition (true forward-chaining)
        if cond_type == 'fact':
            fact = condition.get('fact', '')
            # Support fact templates with variables
            fact = fact.replace('{recipe}', context.get('recipe_id', ''))
            fact = fact.replace('{user}', context.get('user', {}).name if hasattr(context.get('user', {}), 'name') else 'user')
            return self.has_fact(fact)
        
        # Check recipe-specific facts
        elif cond_type == 'recipe_fact':
            recipe_id = context.get('recipe_id', '')
            fact_name = condition.get('fact_name', '')
            expected_value = condition.get('value')
            operator = condition.get('operator', '==')
            
            actual_value = self.get_recipe_fact(recipe_id, fact_name)
            if actual_value is None:
                return False
            
            return self._compare_values(actual_value, expected_value, operator)
        
        # Original attribute-based evaluation (for initial facts)
        obj_name = condition.get('object', 'recipe')
        attribute = condition.get('attribute', '')
        value = condition.get('value')
        operator = condition.get('operator', '==')
        
        obj = context.get(obj_name)
        if obj is None:
            return False
        
        # Handle nested attributes
        if '.' in attribute:
            parts = attribute.split('.')
            attr_value = obj
            for part in parts:
                if hasattr(attr_value, part):
                    attr_value = getattr(attr_value, part)
                else:
                    return False
        # Handle method calls
        elif operator == 'method_call':
            method_name = condition.get('method')
            args = condition.get('args', [])
            if hasattr(obj, method_name):
                method = getattr(obj, method_name)
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
                return method(*resolved_args)
            return False
        else:
            if not hasattr(obj, attribute):
                return False
            attr_value = getattr(obj, attribute)
        
        from enum import Enum
        if isinstance(attr_value, Enum):
            attr_value = attr_value.value
        
        # Resolve value if it's a reference like "recipe.cost" or "user.budget"
        resolved_value = value
        if isinstance(value, str) and '.' in value:
            parts = value.split('.')
            obj_name = parts[0]
            attr_path = parts[1:]
            if obj_name in context:
                resolved_value = context[obj_name]
                for attr_name in attr_path:
                    if hasattr(resolved_value, attr_name):
                        resolved_value = getattr(resolved_value, attr_name)
                    else:
                        resolved_value = value
                        break
        
        return self._compare_values(attr_value, resolved_value, operator)
    
    def _compare_values(self, actual, expected, operator: str) -> bool:
        """Compare two values using the given operator"""
        if operator == '==':
            return actual == expected
        elif operator == '!=':
            return actual != expected
        elif operator == '>':
            return actual > expected
        elif operator == '<':
            return actual < expected
        elif operator == '>=':
            return actual >= expected
        elif operator == '<=':
            return actual <= expected
        elif operator == 'in':
            return actual in expected if isinstance(expected, (list, tuple)) else False
        elif operator == 'not_in':
            return actual not in expected if isinstance(expected, (list, tuple)) else True
        elif operator == 'contains':
            return expected in actual if hasattr(actual, '__contains__') else False
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
    
    def forward_chain(self, person: Any, kitchen: Any, recipes: List[Any], max_iterations: int = 20) -> List[Any]:
        """
        TRUE FORWARD-CHAINING INFERENCE
        
        1. Load initial facts from user and recipes into working memory
        2. Repeat until fixed point (no new facts):
           a. Find rules whose conditions match current facts
           b. Fire rules to assert NEW facts
           c. Track what changed
        3. Use final facts to determine recommendations
        
        This is NOT filtering - we're deriving new knowledge!
        """
        # Reset inference state
        self.clear_working_memory()
        for rule in self.rules:
            rule.fired_count = 0
        
        # Step 1: Assert initial facts from domain objects
        self._load_initial_facts(person, kitchen, recipes)
        
        # Step 2: Forward-chaining loop (fire rules until fixed point)
        iteration = 0
        new_facts_derived = True
        
        while new_facts_derived and iteration < max_iterations:
            new_facts_derived = False
            iteration += 1
            
            # Try to fire each rule
            for rule in self.rules:
                # Build context for each recipe
                for recipe in recipes:
                    recipe_id = recipe.name  # Use name as unique ID
                    context = {
                        'user': person,
                        'person': person,
                        'kitchen': kitchen,
                        'recipe': recipe,
                        'recipe_id': recipe_id
                    }
                    
                    # Check if rule conditions are satisfied
                    if self.evaluate_conditions(rule.conditions, context):
                        # Fire rule to assert new facts
                        facts_changed = self.execute_forward_action(rule, recipe, context, recipe_id)
                        
                        if facts_changed:
                            new_facts_derived = True
                            rule.fired_count += 1
                            if rule.id not in self.fired_rules:
                                self.fired_rules.append(rule.id)
                            
                            # Log inference step
                            self.inference_log.append({
                                'iteration': iteration,
                                'rule': rule.id,
                                'recipe': recipe_id,
                                'description': rule.description
                            })
        
        # Step 3: Extract recommendations from final facts
        return self.get_recommended_recipes(recipes)
    
    def _load_initial_facts(self, person: Any, kitchen: Any, recipes: List[Any]):
        """Load initial facts from domain objects into working memory"""
        # Assert user preference facts
        if hasattr(person, 'allergies'):
            for allergy in person.allergies:
                self.assert_fact(f"user_allergic_to({allergy.lower()})")
        
        if hasattr(person, 'dietary_restrictions'):
            for restriction in person.dietary_restrictions:
                self.assert_fact(f"user_diet({restriction.lower()})")
        
        if hasattr(person, 'skill_level'):
            self.assert_fact(f"user_skill_level({person.skill_level.lower()})")
        
        if hasattr(person, 'budget'):
            self.assert_fact(f"user_budget({person.budget})")
        
        # Assert kitchen facts
        if hasattr(kitchen, 'available_equipment'):
            for equipment in kitchen.available_equipment:
                self.assert_fact(f"has_equipment({equipment.lower()})")
        
        # Initialize recipe facts (all recipes start as "unknown")
        for recipe in recipes:
            recipe_id = recipe.name
            self.set_recipe_fact(recipe_id, 'suitable_for_user', True)
            self.set_recipe_fact(recipe_id, 'affordable', True)
            self.set_recipe_fact(recipe_id, 'can_prepare', True)
            self.set_recipe_fact(recipe_id, 'skill_appropriate', True)
            self.set_recipe_fact(recipe_id, 'recommendation_score', 0.0)
            self.set_recipe_fact(recipe_id, 'exclusion_reasons', [])
            self.set_recipe_fact(recipe_id, 'substitutions', {})
    
    def execute_forward_action(self, rule: Rule, recipe: Any, context: Dict[str, Any], recipe_id: str) -> bool:
        """
        Execute rule action - ASSERT NEW FACTS (forward-chaining)
        
        This is the key difference from filtering:
        - Filtering: removes recipes from a list
        - Forward-chaining: asserts new facts about recipes
        
        Returns True if new facts were derived, False otherwise.
        """
        action = rule.action
        action_type = action.get('type', 'assert')
        changed = False
        
        if action_type == 'assert':
            # Assert new facts into working memory
            facts = action.get('facts', [])
            for fact_template in facts:
                # Substitute variables in fact template
                fact = fact_template.replace('{recipe}', recipe_id)
                fact = fact.replace('{user}', context.get('user', {}).name if hasattr(context.get('user', {}), 'name') else 'user')
                
                if self.assert_fact(fact):
                    changed = True
        
        elif action_type == 'set_recipe_fact':
            # Set a specific fact about this recipe
            fact_name = action.get('fact_name', '')
            value = action.get('value')
            
            # Handle special values
            if value == 'False':
                value = False
            elif value == 'True':
                value = True
            
            if self.set_recipe_fact(recipe_id, fact_name, value):
                changed = True
        
        elif action_type == 'add_to_list':
            # Add item to a list fact
            fact_name = action.get('fact_name', '')
            item = action.get('item', '')
            
            current_list = self.get_recipe_fact(recipe_id, fact_name) or []
            if item not in current_list:
                current_list.append(item)
                self.set_recipe_fact(recipe_id, fact_name, current_list)
                changed = True
        
        elif action_type == 'modify_score':
            # Increment/decrement recommendation score
            score_delta = action.get('delta', 0)
            current_score = self.get_recipe_fact(recipe_id, 'recommendation_score') or 0.0
            new_score = current_score + score_delta
            
            if self.set_recipe_fact(recipe_id, 'recommendation_score', new_score):
                changed = True
        
        elif action_type == 'add_substitution':
            # Add ingredient substitution suggestion
            ingredient = action.get('ingredient', '')
            substitute = action.get('substitute', '')
            
            current_subs = self.get_recipe_fact(recipe_id, 'substitutions') or {}
            if ingredient not in current_subs:
                current_subs[ingredient] = substitute
                self.set_recipe_fact(recipe_id, 'substitutions', current_subs)
                changed = True
        
        return changed
    
    def get_recommended_recipes(self, recipes: List[Any]) -> List[Any]:
        """
        Extract recommended recipes from final facts (after inference)
        
        A recipe is recommended if:
        - suitable_for_user = True (no allergies, diet compatible)
        - affordable = True (within budget)
        - can_prepare = True (has equipment)
        - skill_appropriate = True (user can cook it)
        
        Sorted by recommendation_score (derived facts)
        """
        recommended = []
        
        for recipe in recipes:
            recipe_id = recipe.name
            
            # Check derived facts
            suitable = self.get_recipe_fact(recipe_id, 'suitable_for_user')
            affordable = self.get_recipe_fact(recipe_id, 'affordable')
            can_prepare = self.get_recipe_fact(recipe_id, 'can_prepare')
            skill_ok = self.get_recipe_fact(recipe_id, 'skill_appropriate')
            score = self.get_recipe_fact(recipe_id, 'recommendation_score') or 0.0
            
            # Apply facts back to recipe object (for compatibility)
            recipe.suitable_for_user = suitable if suitable is not None else True
            recipe.affordable = affordable if affordable is not None else True
            recipe.can_prepare = can_prepare if can_prepare is not None else True
            recipe.skill_appropriate = skill_ok if skill_ok is not None else True
            recipe.recommendation_score = score
            recipe.exclusion_reasons = self.get_recipe_fact(recipe_id, 'exclusion_reasons') or []
            recipe.substitution_suggestions = self.get_recipe_fact(recipe_id, 'substitutions') or {}
            
            if suitable and affordable and can_prepare and skill_ok:
                recommended.append(recipe)
        
        recommended.sort(key=lambda r: r.recommendation_score, reverse=True)
        
        return recommended
    
    def get_inference_explanation(self, recipe_name: str) -> Dict[str, Any]:
        """Get explanation of why a recipe was/wasn't recommended"""
        facts = self.recipe_facts.get(recipe_name, {})
        relevant_rules = [log for log in self.inference_log if log['recipe'] == recipe_name]
        
        return {
            'recipe': recipe_name,
            'facts': facts,
            'rules_fired': relevant_rules,
            'is_recommended': facts.get('suitable_for_user', False) and 
                            facts.get('affordable', False) and
                            facts.get('can_prepare', False) and
                            facts.get('skill_appropriate', False)
        }
