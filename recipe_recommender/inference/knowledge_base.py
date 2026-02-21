"""
Knowledge base management
"""

from typing import List, Dict, Any
import yaml
import json
from pathlib import Path


class KnowledgeBase:
    """Manages rules and domain knowledge"""
    
    def __init__(self, kb_path: str = None):
        self.rules: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
        
        if kb_path:
            self.load(kb_path)
    
    def load(self, kb_path: str):
        """Load knowledge base from file"""
        path = Path(kb_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Knowledge base file not found: {kb_path}")
        
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif path.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
        
        self.rules = data.get('rules', [])
        self.metadata = data.get('metadata', {})
    
    def save(self, kb_path: str):
        """Save knowledge base to file"""
        path = Path(kb_path)
        
        data = {
            'metadata': self.metadata,
            'rules': self.rules
        }
        
        with open(path, 'w') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(data, f, default_flow_style=False)
            elif path.suffix == '.json':
                json.dump(data, f, indent=2)
    
    def add_rule(self, rule: Dict[str, Any]):
        """Add a rule to the knowledge base"""
        self.rules.append(rule)
    
    def get_rules(self, category: str = None) -> List[Dict[str, Any]]:
        """Get rules, optionally filtered by category"""
        if category:
            return [r for r in self.rules if r.get('category') == category]
        return self.rules
    
    def get_rule_by_id(self, rule_id: str) -> Dict[str, Any]:
        """Get a specific rule by ID"""
        for rule in self.rules:
            if rule.get('id') == rule_id:
                return rule
        return None
