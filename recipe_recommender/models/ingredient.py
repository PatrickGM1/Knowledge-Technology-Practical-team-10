"""
Ingredient model for recipe recommendation system.
Represents a recipe ingredient with properties and substitution options.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Ingredient:
    """Represents a recipe ingredient"""
    
    name: str
    quantity: float
    unit: str
    category: str = "other"
    is_optional: bool = False
    substitutes: Dict[str, float] = field(default_factory=dict)  # {substitute_name: conversion_ratio}
    allergens: List[str] = field(default_factory=list)
    dietary_flags: List[str] = field(default_factory=list)
    preparation: Optional[str] = None
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        prep = f", {self.preparation}" if self.preparation else ""
        optional = " (optional)" if self.is_optional else ""
        return f"{self.quantity} {self.unit} {self.name}{prep}{optional}"
    
    def has_allergen(self, allergen: str) -> bool:
        """Check if ingredient contains a specific allergen."""
        return allergen.lower() in [a.lower() for a in self.allergens]
    
    def is_suitable_for_diet(self, dietary_restriction: str) -> bool:
        """Check if ingredient is suitable for a specific diet."""
        return dietary_restriction.lower() in [d.lower() for d in self.dietary_flags]
    
    def get_substitute(self, substitute_name: str) -> Optional[float]:
        """Get the conversion ratio for a specific substitute."""
        for sub, ratio in self.substitutes.items():
            if sub.lower() == substitute_name.lower():
                return ratio
        return None
    
    def get_substitutes_for_diet(self, dietary_restriction: str) -> List[str]:
        """Get substitutes that are suitable for a specific diet."""
        # This would ideally query a knowledge base
        # For now, returning list of substitute names
        return list(self.substitutes.keys())
    
    def convert_quantity(self, new_servings: int, original_servings: int) -> 'Ingredient':
        """Create a new Ingredient with quantity adjusted for different servings."""
        ratio = new_servings / original_servings
        return Ingredient(
            name=self.name,
            quantity=self.quantity * ratio,
            unit=self.unit,
            category=self.category,
            is_optional=self.is_optional,
            substitutes=self.substitutes.copy(),
            allergens=self.allergens.copy(),
            dietary_flags=self.dietary_flags.copy(),
            preparation=self.preparation
        )


# Common ingredient categories
INGREDIENT_CATEGORIES = {
    'protein': ['chicken', 'beef', 'pork', 'fish', 'tofu', 'beans', 'lentils', 'eggs'],
    'vegetable': ['tomato', 'onion', 'garlic', 'carrot', 'celery', 'spinach', 'kale'],
    'grain': ['rice', 'pasta', 'bread', 'flour', 'quinoa', 'oats'],
    'dairy': ['milk', 'cheese', 'butter', 'yogurt', 'cream'],
    'spice': ['salt', 'pepper', 'cumin', 'paprika', 'oregano', 'basil'],
    'oil': ['olive oil', 'vegetable oil', 'coconut oil', 'butter'],
    'sweetener': ['sugar', 'honey', 'maple syrup', 'agave'],
    'other': []
}
