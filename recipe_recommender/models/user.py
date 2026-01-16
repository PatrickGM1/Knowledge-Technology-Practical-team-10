"""
User model for recipe recommendation system.
Represents a user with dietary preferences, restrictions, and cooking profile.
"""

from typing import List, Optional, Dict, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from .allergy import Allergy
    from .budget_constraint import BudgetConstraint
    from .cooking_skill import CookingSkill
    from .time_constraint import TimeConstraint
    from .dietary_preference import DietaryPreference
    from .health_goal import HealthGoal
    from .kitchen import Kitchen


@dataclass
class User:
    """Represents a user with dietary preferences and cooking profile
    
    DEPRECATED attributes (kept for backward compatibility):
    - dietary_restrictions: Use dietary_preference instead
    - allergies: Use allergies_list instead
    - skill_level: Use skill instead
    - available_equipment: Use kitchen instead
    - max_cooking_time: Use time_constraint instead
    - health_goals: Use health_goals_list instead
    """
    
    name: str
    
    # Legacy attributes (deprecated but kept for compatibility)
    dietary_restrictions: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    preferences: Dict[str, bool] = field(default_factory=dict)
    disliked_ingredients: List[str] = field(default_factory=list)
    skill_level: str = "beginner"  # beginner, intermediate, advanced
    available_equipment: List[str] = field(default_factory=list)
    max_cooking_time: Optional[int] = None  # in minutes
    calorie_target: Optional[int] = None  # daily calorie target
    cuisine_preferences: List[str] = field(default_factory=list)
    health_goals: List[str] = field(default_factory=list)
    
    # New domain class attributes
    allergies_list: Optional[List['Allergy']] = None
    budget: Optional['BudgetConstraint'] = None
    skill: Optional['CookingSkill'] = None
    time_constraint: Optional['TimeConstraint'] = None
    dietary_preference: Optional['DietaryPreference'] = None
    health_goals_list: Optional[List['HealthGoal']] = None
    kitchen: Optional['Kitchen'] = None
    
    def has_dietary_restriction(self, restriction: str) -> bool:
        """Check if user has a specific dietary restriction."""
        return restriction.lower() in [r.lower() for r in self.dietary_restrictions]
    
    def is_allergic_to(self, ingredient: str) -> bool:
        """Check if user is allergic to a specific ingredient."""
        return ingredient.lower() in [a.lower() for a in self.allergies]
    
    def dislikes_ingredient(self, ingredient: str) -> bool:
        """Check if user dislikes a specific ingredient."""
        return ingredient.lower() in [i.lower() for i in self.disliked_ingredients]
    
    def has_equipment(self, equipment: str) -> bool:
        """Check if user has specific cooking equipment."""
        return equipment.lower() in [e.lower() for e in self.available_equipment]
    
    def can_cook_complexity(self, complexity: str) -> bool:
        """Check if user's skill level matches or exceeds required complexity."""
        skill_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        user_level = skill_levels.get(self.skill_level.lower(), 1)
        required_level = skill_levels.get(complexity.lower(), 1)
        return user_level >= required_level
    
    def within_time_constraint(self, cooking_time: int) -> bool:
        """Check if cooking time is within user's constraint."""
        if self.max_cooking_time is None:
            return True
        return cooking_time <= self.max_cooking_time
    
    def prefers_cuisine(self, cuisine: str) -> bool:
        """Check if user prefers a specific cuisine."""
        if not self.cuisine_preferences:
            return True  # No preference means all cuisines are acceptable
        return cuisine.lower() in [c.lower() for c in self.cuisine_preferences]
