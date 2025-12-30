"""
Equipment model for recipe recommendation system.
Represents cooking equipment needed for recipes.
"""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Equipment:
    """Represents cooking equipment"""
    
    name: str
    category: str = "utensil"
    is_essential: bool = True
    alternatives: List[str] = field(default_factory=list)
    description: Optional[str] = None
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        essential = " (essential)" if self.is_essential else " (optional)"
        return f"{self.name}{essential}"
    
    def has_alternative(self, alternative_name: str) -> bool:
        """Check if a specific alternative exists for this equipment."""
        return alternative_name.lower() in [a.lower() for a in self.alternatives]
    
    def get_alternatives(self) -> List[str]:
        """Get list of alternative equipment."""
        return self.alternatives.copy()


# Common equipment categories and examples
EQUIPMENT_CATEGORIES = {
    'cookware': ['pot', 'pan', 'skillet', 'wok', 'dutch oven', 'saucepan', 'stockpot'],
    'bakeware': ['baking sheet', 'cake pan', 'muffin tin', 'loaf pan', 'pie dish', 'casserole dish'],
    'appliance': ['oven', 'stove', 'microwave', 'blender', 'food processor', 'mixer', 'slow cooker', 'air fryer'],
    'utensil': ['knife', 'spatula', 'whisk', 'tongs', 'ladle', 'peeler', 'grater', 'measuring cups'],
    'specialized': ['thermometer', 'rolling pin', 'sieve', 'colander', 'mortar and pestle']
}

# Common equipment substitutions
EQUIPMENT_SUBSTITUTIONS = {
    'food processor': ['blender', 'hand chopper', 'knife and cutting board'],
    'stand mixer': ['hand mixer', 'whisk and bowl'],
    'dutch oven': ['large pot with lid', 'slow cooker'],
    'air fryer': ['oven', 'deep fryer'],
    'wok': ['large skillet', 'saute pan'],
    'blender': ['food processor', 'immersion blender'],
    'baking sheet': ['cake pan', 'pizza pan'],
    'muffin tin': ['ramekins', 'small baking dishes']
}
