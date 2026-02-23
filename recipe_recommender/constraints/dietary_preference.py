"""
Dietary preference model for recipe recommendation system
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class DietaryPreference:
    """Represents dietary preferences and restrictions"""
    
    type: str = "omnivore"
    restrictions: List[str] = field(default_factory=list)
    preferred_cuisines: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.restrictions:
            self.restrictions = []
        
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
        if not hasattr(recipe, 'diet'):
            return True
        
        recipe_diet = recipe.diet
        if hasattr(recipe_diet, 'value'):
            recipe_diet_str = recipe_diet.value.lower()
        else:
            recipe_diet_str = str(recipe_diet).lower()
        
        user_diet = self.type.lower()
        
        if user_diet == 'vegan':
            return recipe_diet_str == 'vegan'
        elif user_diet == 'vegetarian':
            return recipe_diet_str in ['vegan', 'vegetarian']
        elif user_diet == 'pescatarian':
            return recipe_diet_str in ['vegan', 'vegetarian', 'pescatarian']
        else:
            return True
    
    def prefers_cuisine(self, cuisine: str) -> bool:
        if not self.preferred_cuisines:
            return True
        
        cuisine_lower = cuisine.lower() if cuisine else ""
        return any(pref.lower() in cuisine_lower or cuisine_lower in pref.lower() 
                  for pref in self.preferred_cuisines)
    
    def has_restriction(self, restriction: str) -> bool:
        restriction_lower = restriction.lower()
        return any(r.lower() == restriction_lower for r in self.restrictions)
