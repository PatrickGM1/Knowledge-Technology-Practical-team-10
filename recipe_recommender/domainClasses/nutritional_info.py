"""
Nutritional Info Domain Class
Represents the nutritional content of a recipe
"""

from typing import Dict
from dataclasses import dataclass, field


@dataclass
class NutritionalInfo:
    """Represents nutritional information for a recipe"""
    
    calories: float = 0.0
    protein: float = 0.0
    carbohydrates: float = 0.0
    fat: float = 0.0
    
    saturated_fat: float = 0.0
    fiber: float = 0.0
    sugar: float = 0.0
    
    sodium: float = 0.0
    cholesterol: float = 0.0
    vitamins: Dict[str, float] = field(default_factory=dict)
    minerals: Dict[str, float] = field(default_factory=dict)
    
    serving_size: str = "1 serving"
    servings_per_recipe: int = 1
    
    # User-friendly string for nutrition info
    def __str__(self) -> str:
        return (f"Calories: {self.calories}, Protein: {self.protein}g, "
                f"Carbs: {self.carbohydrates}g, Fat: {self.fat}g")
    
    # Check if calories are below a threshold
    def is_low_calorie(self, threshold: float = 400.0) -> bool:
        return self.calories < threshold
    
    # Check if protein is above a threshold
    def is_high_protein(self, threshold: float = 20.0) -> bool:
        return self.protein >= threshold
    
    # Check if carbs are below a threshold
    def is_low_carb(self, threshold: float = 30.0) -> bool:
        return self.carbohydrates < threshold
    
    # Check if fat is below a threshold
    def is_low_fat(self, threshold: float = 10.0) -> bool:
        return self.fat < threshold
    
    # Check if fiber is above a threshold
    def is_high_fiber(self, threshold: float = 5.0) -> bool:
        return self.fiber >= threshold
    
    # Check if sodium is below a threshold
    def is_low_sodium(self, threshold: float = 500.0) -> bool:
        return self.sodium < threshold
    
    # Check if recipe is heart healthy
    def is_heart_healthy(self) -> bool:
        return self.saturated_fat < 5.0 and self.sodium < 400.0
    
    # Get calorie density as low/medium/high
    def get_calorie_density(self) -> str:
        if self.calories < 300:
            return "low"
        elif self.calories < 500:
            return "medium"
        else:
            return "high"
    
    # Calculate percentage of calories from macros
    def get_macro_balance(self) -> Dict[str, float]:
        """Calculate percentage of calories from each macronutrient"""
        protein_cal = self.protein * 4
        carb_cal = self.carbohydrates * 4
        fat_cal = self.fat * 9
        total = protein_cal + carb_cal + fat_cal
        
        if total == 0:
            return {"protein": 0, "carbs": 0, "fat": 0}
        
        return {
            "protein": round((protein_cal / total) * 100, 1),
            "carbs": round((carb_cal / total) * 100, 1),
            "fat": round((fat_cal / total) * 100, 1)
        }
