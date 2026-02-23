"""
Allergy model for recipe recommendation system
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Allergy:
    """Represents an allergy with associated unsafe ingredients"""
    
    allergen_name: str
    ingredients_to_avoid: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.ingredients_to_avoid:
            self.ingredients_to_avoid = self._get_default_ingredients()
    
    def _get_default_ingredients(self) -> List[str]:
        allergen_map = {
            'nuts': ['nuts', 'almonds', 'walnuts', 'pecans', 'cashews', 'peanuts', 
                    'almond butter', 'peanut butter', 'nut butter'],
            'dairy': ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'whey', 
                     'lactose', 'casein', 'parmesan', 'pecorino', 'mozzarella'],
            'gluten': ['flour', 'wheat', 'bread', 'pasta', 'barley', 'rye', 
                      'soy sauce', 'wheat flour', 'all-purpose flour'],
            'eggs': ['eggs', 'egg', 'mayonnaise', 'meringue'],
            'soy': ['soy', 'tofu', 'tempeh', 'soy sauce', 'edamame'],
            'shellfish': ['shrimp', 'crab', 'lobster', 'prawns', 'scallops'],
            'fish': ['fish', 'salmon', 'tuna', 'cod', 'halibut', 'anchovy']
        }
        
        allergen_lower = self.allergen_name.lower()
        return allergen_map.get(allergen_lower, [allergen_lower])
    
    def is_safe(self, ingredient) -> bool:
        ingredient_name = ingredient.name if hasattr(ingredient, 'name') else str(ingredient)
        ingredient_lower = ingredient_name.lower()
        
        for avoid in self.ingredients_to_avoid:
            if avoid.lower() in ingredient_lower or ingredient_lower in avoid.lower():
                return False
        
        if hasattr(ingredient, 'allergens'):
            for allergen in ingredient.allergens:
                if allergen.lower() == self.allergen_name.lower():
                    return False
        
        return True
    
    def __str__(self) -> str:
        return f"{self.allergen_name} allergy"
