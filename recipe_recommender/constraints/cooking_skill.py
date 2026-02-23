"""
Cooking skill model for recipe recommendation system
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class CookingSkill:
    """Represents a user's cooking skill level and experience"""
    
    level: str = "beginner"
    years_experience: int = 0
    comfortable_techniques: List[str] = field(default_factory=list)
    learned_recipes: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.comfortable_techniques:
            self.comfortable_techniques = self._get_default_techniques()
    
    def _get_default_techniques(self) -> List[str]:
        all_techniques = {
            'beginner': ['boiling', 'simmering', 'pan-frying', 'basic knife skills'],
            'intermediate': ['sautéing', 'roasting', 'baking', 'grilling', 'steaming', 
                           'intermediate knife skills', 'sauce making'],
            'advanced': ['braising', 'sous-vide', 'advanced knife skills', 'filleting', 
                        'pastry making', 'fermentation', 'reduction sauces']
        }
        
        techniques = []
        level_lower = self.level.lower()
        
        if level_lower in ['beginner', 'intermediate', 'advanced']:
            techniques.extend(all_techniques['beginner'])
        if level_lower in ['intermediate', 'advanced']:
            techniques.extend(all_techniques['intermediate'])
        if level_lower == 'advanced':
            techniques.extend(all_techniques['advanced'])
        
        return techniques
    
    def can_handle(self, recipe_or_complexity) -> bool:
        if hasattr(recipe_or_complexity, 'skill'):
            recipe_complexity = recipe_or_complexity.skill.value if hasattr(recipe_or_complexity.skill, 'value') else str(recipe_or_complexity.skill)
        else:
            recipe_complexity = recipe_or_complexity
        
        complexity_map = {
            'easy': 'beginner',
            'medium': 'intermediate',
            'experienced': 'advanced',
            'beginner': 'beginner',
            'intermediate': 'intermediate',
            'advanced': 'advanced'
        }
        
        normalized_complexity = complexity_map.get(recipe_complexity.lower(), recipe_complexity.lower())
        normalized_level = complexity_map.get(self.level.lower(), self.level.lower())
        
        skill_order = ['beginner', 'intermediate', 'advanced']
        
        try:
            user_level_idx = skill_order.index(normalized_level)
            recipe_level_idx = skill_order.index(normalized_complexity)
            return user_level_idx >= recipe_level_idx
        except ValueError:
            return True
    
    def can_perform_technique(self, technique: str) -> bool:
        technique_lower = technique.lower()
        return any(tech.lower() in technique_lower or technique_lower in tech.lower() 
                  for tech in self.comfortable_techniques)
    
    def has_learned(self, recipe_name: str) -> bool:
        return recipe_name.lower() in [r.lower() for r in self.learned_recipes]
    
    def get_skill_level_number(self) -> int:
        skill_map = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        return skill_map.get(self.level.lower(), 1)
