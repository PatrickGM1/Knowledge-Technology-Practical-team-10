"""
Health goal model for recipe recommendation system
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HealthGoal:
    """Represents a health or nutritional goal"""
    
    goal_type: str
    target_value: Optional[float] = None
    priority: str = "medium"
    
    # Check if nutritional info matches the health goal
    def matches(self, nutritional_info) -> bool:
        if not nutritional_info:
            return False
        
        goal_lower = self.goal_type.lower()
        
        if goal_lower == 'high-protein':
            threshold = self.target_value if self.target_value else 20.0
            return hasattr(nutritional_info, 'is_high_protein') and nutritional_info.is_high_protein(threshold)
        
        elif goal_lower == 'low-carb':
            threshold = self.target_value if self.target_value else 30.0
            return hasattr(nutritional_info, 'is_low_carb') and nutritional_info.is_low_carb(threshold)
        
        elif goal_lower == 'low-fat':
            threshold = self.target_value if self.target_value else 10.0
            return hasattr(nutritional_info, 'is_low_fat') and nutritional_info.is_low_fat(threshold)
        
        elif goal_lower == 'low-calorie':
            threshold = self.target_value if self.target_value else 400.0
            return hasattr(nutritional_info, 'is_low_calorie') and nutritional_info.is_low_calorie(threshold)
        
        elif goal_lower == 'high-fiber':
            threshold = self.target_value if self.target_value else 5.0
            return hasattr(nutritional_info, 'is_high_fiber') and nutritional_info.is_high_fiber(threshold)
        
        elif goal_lower == 'low-sodium':
            threshold = self.target_value if self.target_value else 600.0
            return hasattr(nutritional_info, 'is_low_sodium') and nutritional_info.is_low_sodium(threshold)
        
        elif goal_lower in ['low-sugar', 'low-sugars']:
            if hasattr(nutritional_info, 'sugar'):
                threshold = self.target_value if self.target_value else 10.0
                return nutritional_info.sugar < threshold
            return False
        
        elif hasattr(nutritional_info, 'fits_health_goal'):
            return nutritional_info.fits_health_goal(goal_lower)
        
        return False
    
    # Get numeric priority level
    def get_priority_level(self) -> int:
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        return priority_map.get(self.priority.lower(), 2)
    
    # Get a human-readable description of the goal
    def get_goal_description(self) -> str:
        descriptions = {
            'high-protein': 'High Protein',
            'low-carb': 'Low Carbohydrates',
            'low-fat': 'Low Fat',
            'low-calorie': 'Low Calorie',
            'high-fiber': 'High Fiber',
            'low-sodium': 'Low Sodium',
            'low-sugar': 'Low Sugar',
            'low-sugars': 'Low Sugar'
        }
        return descriptions.get(self.goal_type.lower(), self.goal_type.title())
    
    # User-friendly string for the health goal
    def __str__(self) -> str:
        target = f" (target: {self.target_value})" if self.target_value else ""
        return f"{self.get_goal_description()}{target}"
