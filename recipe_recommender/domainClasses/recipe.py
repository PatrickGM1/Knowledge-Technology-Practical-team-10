"""
Recipe Domain Class
Represents a cooking recipe - the core domain concept
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Recipe:
    """Represents a complete cooking recipe"""
    
    name: str
    description: str = ""
    
    ingredients: List = field(default_factory=list)
    equipment: List = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    
    prep_time: int = 0
    cook_time: int = 0
    total_time: int = 0
    servings: int = 4
    
    cuisine: str = ""
    meal: str = ""
    
    diet: str = "omnivore"
    diet_restrictions: List[str] = field(default_factory=list)
    
    cooking_time: str = "15 to 45 minutes"
    skill: str = "medium"
    cooking_methods: List[str] = field(default_factory=list)
    
    nutritional_info: Optional[object] = None
    macros: List[str] = field(default_factory=list)
    
    budget: str = "moderate"
    cost: float = 0.0
    
    tags: List[str] = field(default_factory=list)
    image_url: str = ""
    
    suitable_for_user: bool = True
    affordable: bool = True
    can_prepare: bool = True
    skill_appropriate: bool = True
    recommendation_score: float = 0.0
    exclusion_reasons: List[str] = field(default_factory=list)
    substitution_suggestions: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.total_time == 0:
            self.total_time = self.prep_time + self.cook_time
    
    def __repr__(self) -> str:
        return f"Recipe(name='{self.name}', diet={self.diet}, meal={self.meal})"
    
    def __str__(self) -> str:
        return f"{self.name} - {self.diet} {self.meal}"
    
    def has_ingredient(self, *ingredient_names: str) -> bool:
        """Check if recipe contains any of the specified ingredients"""
        for target_name in ingredient_names:
            for ing in self.ingredients:
                ing_name = ing.name if hasattr(ing, 'name') else str(ing)
                if target_name.lower() in ing_name.lower():
                    return True
        return False
    
    def has_equipment(self, equipment_name: str) -> bool:
        """Check if recipe requires specific equipment"""
        for eq in self.equipment:
            eq_name = eq.name if hasattr(eq, 'name') else str(eq)
            if equipment_name.lower() in eq_name.lower():
                return True
        return False
    
    def matches_diet(self, diet: str) -> bool:
        """Check if recipe matches a specific diet type"""
        return self.diet.lower() == diet.lower()
    
    def matches_meal(self, meal: str) -> bool:
        """Check if recipe is for a specific meal type"""
        return self.meal.lower() == meal.lower()
    
    def is_quick(self) -> bool:
        """Check if recipe is quick (less than 15 minutes)"""
        return self.cooking_time == "less than 15 minutes"
    
    def is_budget_friendly(self) -> bool:
        """Check if recipe is budget-friendly"""
        return self.budget == "low_cost"
