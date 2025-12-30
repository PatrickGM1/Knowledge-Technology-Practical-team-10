"""
Nutritional information model for recipe recommendation system.
Represents nutritional data for recipes.
"""

from typing import Optional, Dict
from dataclasses import dataclass, field


@dataclass
class NutritionalInfo:
    """Represents nutritional information for a recipe"""
    
    calories: float = 0.0
    protein: float = 0.0  # grams
    carbohydrates: float = 0.0  # grams
    fat: float = 0.0  # grams
    saturated_fat: float = 0.0  # grams
    fiber: float = 0.0  # grams
    sugar: float = 0.0  # grams
    sodium: float = 0.0  # milligrams
    cholesterol: float = 0.0  # milligrams
    vitamins: Dict[str, float] = field(default_factory=dict)  # {vitamin_name: amount}
    minerals: Dict[str, float] = field(default_factory=dict)  # {mineral_name: amount}
    serving_size: str = "1 serving"
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return (f"Calories: {self.calories}, "
                f"Protein: {self.protein}g, "
                f"Carbs: {self.carbohydrates}g, "
                f"Fat: {self.fat}g")
    
    def is_low_calorie(self, threshold: int = 400) -> bool:
        """Check if recipe is low calorie (default threshold: 400 calories)."""
        return self.calories < threshold
    
    def is_high_protein(self, threshold: float = 20.0) -> bool:
        """Check if recipe is high in protein (default threshold: 20g)."""
        return self.protein >= threshold
    
    def is_low_carb(self, threshold: float = 30.0) -> bool:
        """Check if recipe is low in carbohydrates (default threshold: 30g)."""
        return self.carbohydrates < threshold
    
    def is_low_fat(self, threshold: float = 10.0) -> bool:
        """Check if recipe is low in fat (default threshold: 10g)."""
        return self.fat < threshold
    
    def is_high_fiber(self, threshold: float = 5.0) -> bool:
        """Check if recipe is high in fiber (default threshold: 5g)."""
        return self.fiber >= threshold
    
    def is_low_sodium(self, threshold: float = 600.0) -> bool:
        """Check if recipe is low in sodium (default threshold: 600mg)."""
        return self.sodium < threshold
    
    def get_macros_ratio(self) -> Dict[str, float]:
        """Calculate the ratio of macronutrients (protein, carbs, fat)."""
        total = self.protein + self.carbohydrates + self.fat
        if total == 0:
            return {'protein': 0, 'carbohydrates': 0, 'fat': 0}
        
        return {
            'protein': (self.protein / total) * 100,
            'carbohydrates': (self.carbohydrates / total) * 100,
            'fat': (self.fat / total) * 100
        }
    
    def fits_health_goal(self, health_goal: str) -> bool:
        """Check if nutritional info fits a specific health goal."""
        goal_checks = {
            'low-carb': self.is_low_carb(),
            'high-protein': self.is_high_protein(),
            'low-fat': self.is_low_fat(),
            'low-calorie': self.is_low_calorie(),
            'high-fiber': self.is_high_fiber(),
            'low-sodium': self.is_low_sodium(),
            'heart-healthy': self.is_low_sodium() and self.is_low_fat(),
            'weight-loss': self.is_low_calorie() and self.is_high_fiber(),
            'muscle-building': self.is_high_protein(),
            'keto': self.is_low_carb() and self.fat > 15.0,
            'balanced': 15 <= self.get_macros_ratio()['protein'] <= 35
        }
        
        return goal_checks.get(health_goal.lower(), False)
    
    def scale_for_servings(self, servings: int, original_servings: int = 1) -> 'NutritionalInfo':
        """Create a new NutritionalInfo scaled for different number of servings."""
        ratio = servings / original_servings
        
        return NutritionalInfo(
            calories=self.calories * ratio,
            protein=self.protein * ratio,
            carbohydrates=self.carbohydrates * ratio,
            fat=self.fat * ratio,
            saturated_fat=self.saturated_fat * ratio,
            fiber=self.fiber * ratio,
            sugar=self.sugar * ratio,
            sodium=self.sodium * ratio,
            cholesterol=self.cholesterol * ratio,
            vitamins={k: v * ratio for k, v in self.vitamins.items()},
            minerals={k: v * ratio for k, v in self.minerals.items()},
            serving_size=self.serving_size
        )
