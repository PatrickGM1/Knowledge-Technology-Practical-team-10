"""
User model for recipe recommendation system
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class User:
    """Represents a user with dietary preferences and cooking profile"""
    
    name: str
    
    dietary_restrictions: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    preferences: Dict[str, bool] = field(default_factory=dict)
    disliked_ingredients: List[str] = field(default_factory=list)
    skill_level: str = "beginner"
    available_equipment: List[str] = field(default_factory=list)
    max_cooking_time: Optional[int] = None
    calorie_target: Optional[int] = None
    cuisine_preferences: List[str] = field(default_factory=list)
    health_goals: List[str] = field(default_factory=list)
    budget: float = 20.0
    
    def has_dietary_restriction(self, restriction: str) -> bool:
        return restriction.lower() in [r.lower() for r in self.dietary_restrictions]
    
    def is_allergic_to(self, ingredient: str) -> bool:
        return ingredient.lower() in [a.lower() for a in self.allergies]
    
    def dislikes_ingredient(self, ingredient: str) -> bool:
        return ingredient.lower() in [i.lower() for i in self.disliked_ingredients]
    
    def has_equipment(self, equipment: str) -> bool:
        return equipment.lower() in [e.lower() for e in self.available_equipment]
    
    def can_cook_complexity(self, complexity: str) -> bool:
        skill_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        user_level = skill_levels.get(self.skill_level.lower(), 1)
        required_level = skill_levels.get(complexity.lower(), 1)
        return user_level >= required_level
    
    def within_time_constraint(self, cooking_time: int) -> bool:
        if self.max_cooking_time is None:
            return True
        return cooking_time <= self.max_cooking_time
    
    def prefers_cuisine(self, cuisine: str) -> bool:
        if not self.cuisine_preferences:
            return True
        return cuisine.lower() in [c.lower() for c in self.cuisine_preferences]
