"""
Ingredient Domain Class
Represents a food item used in recipes
"""

from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class Ingredient:
    """Represents an ingredient in a recipe"""
    
    name: str
    quantity: float = 0.0
    unit: str = ""
    
    category: str = "other"
    is_optional: bool = False
    preparation: str = ""
    
    allergens: List[str] = field(default_factory=list)
    dietary_flags: List[str] = field(default_factory=list)
    substitutes: Dict[str, float] = field(default_factory=dict)
    
    is_protein_source: bool = False
    is_carb_source: bool = False
    is_fat_source: bool = False
    
    def __str__(self) -> str:
        optional = " (optional)" if self.is_optional else ""
        prep = f", {self.preparation}" if self.preparation else ""
        if self.quantity > 0 and self.unit:
            return f"{self.quantity} {self.unit} {self.name}{prep}{optional}"
        return f"{self.name}{prep}{optional}"
    
    def __repr__(self) -> str:
        return f"Ingredient(name='{self.name}', quantity={self.quantity}, unit='{self.unit}')"
    
    def has_allergen(self, allergen: str) -> bool:
        return allergen.lower() in [a.lower() for a in self.allergens]
    
    def is_suitable_for_diet(self, diet: str) -> bool:
        return diet.lower() in [d.lower() for d in self.dietary_flags]
    
    def get_substitute(self, substitute_name: str) -> float:
        for sub, ratio in self.substitutes.items():
            if sub.lower() == substitute_name.lower():
                return ratio
        return 1.0
