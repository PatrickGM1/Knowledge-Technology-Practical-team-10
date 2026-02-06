"""
Dietary preference domain class for recipe recommendation system.
Represents a user's dietary choices and restrictions.
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class DietaryPreference:
    """Represents dietary preferences and restrictions"""
    
    type: str = "omnivore"  # vegan, vegetarian, pescatarian, omnivore
    restrictions: List[str] = field(default_factory=list)
    preferred_cuisines: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Add implicit restrictions based on diet type"""
        if not self.restrictions:
            self.restrictions = []
        
        # Add restrictions implied by diet type
        diet_lower = self.type.lower()
        if diet_lower == 'vegan':
            implicit = ['no-meat', 'no-dairy', 'no-eggs', 'no-honey', 'plant-based']
            for restriction in implicit:
                if restriction not in self.restrictions:
                    self.restrictions.append(restriction)
        elif diet_lower == 'vegetarian':
            implicit = ['no-meat', 'no-fish']
            for restriction in implicit:
                if restriction not in self.restrictions:
                    self.restrictions.append(restriction)
        elif diet_lower == 'pescatarian':
            implicit = ['no-meat']
            for restriction in implicit:
                if restriction not in self.restrictions:
                    self.restrictions.append(restriction)
    
    def is_compatible(self, recipe) -> bool:
        """
        Check if recipe matches dietary preference.
        
        Args:
            recipe: Recipe object with diet attribute
            
        Returns:
            True if recipe is compatible, False otherwise
        """
        if not hasattr(recipe, 'diet'):
            return True  # If no diet info, assume compatible
        
        # Get recipe diet type
        recipe_diet = recipe.diet
        if hasattr(recipe_diet, 'value'):
            recipe_diet_str = recipe_diet.value.lower()
        else:
            recipe_diet_str = str(recipe_diet).lower()
        
        user_diet = self.type.lower()
        
        # Vegan can only eat vegan
        if user_diet == 'vegan':
            return recipe_diet_str == 'vegan'
        
        # Vegetarian can eat vegan or vegetarian
        elif user_diet == 'vegetarian':
            return recipe_diet_str in ['vegan', 'vegetarian']
        
        # Pescatarian can eat vegan, vegetarian, or pescatarian
        elif user_diet == 'pescatarian':
            return recipe_diet_str in ['vegan', 'vegetarian', 'pescatarian']
        
        # Omnivore can eat anything
        else:  # omnivore
            return True
    
    def prefers_cuisine(self, cuisine: str) -> bool:
        """
        Check if user prefers a specific cuisine.
        
        Args:
            cuisine: Cuisine name (e.g., 'Italian', 'Asian', 'Mexican')
            
        Returns:
            True if cuisine is preferred or no preferences set, False otherwise
        """
        if not self.preferred_cuisines:
            return True  # No preference means all cuisines acceptable
        
        cuisine_lower = cuisine.lower() if cuisine else ""
        return any(pref.lower() in cuisine_lower or cuisine_lower in pref.lower() 
                  for pref in self.preferred_cuisines)
    
    def has_restriction(self, restriction: str) -> bool:
        """Check if a specific restriction applies"""
        restriction_lower = restriction.lower()
        return any(r.lower() == restriction_lower for r in self.restrictions)
    
    def get_diet_strictness(self) -> int:
        """Get numeric strictness level (1=omnivore, 2=pescatarian, 3=vegetarian, 4=vegan)"""
        strictness_map = {
            'omnivore': 1,
            'pescatarian': 2,
            'vegetarian': 3,
            'vegan': 4
        }
        return strictness_map.get(self.type.lower(), 1)
    
    def __str__(self) -> str:
        restrictions_str = f" ({len(self.restrictions)} restrictions)" if self.restrictions else ""
        return f"{self.type.title()} diet{restrictions_str}"
    
    def __repr__(self) -> str:
        return f"DietaryPreference(type='{self.type}', restrictions={len(self.restrictions)})"
