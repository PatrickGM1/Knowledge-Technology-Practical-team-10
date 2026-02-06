"""
Health goal domain class for recipe recommendation system.
Represents a user's nutritional or health objectives.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HealthGoal:
    """Represents a health or nutritional goal"""
    
    goal_type: str  # high-protein, low-carb, low-fat, low-calorie, high-fiber, etc.
    target_value: Optional[float] = None
    priority: str = "medium"  # low, medium, high
    
    def matches(self, nutritional_info) -> bool:
        """
        Check if nutritional information matches this health goal.
        
        Args:
            nutritional_info: NutritionalInfo object with nutritional data
            
        Returns:
            True if nutrition matches goal, False otherwise
        """
        if not nutritional_info:
            return False
        
        goal_lower = self.goal_type.lower()
        
        # High protein goal (>= 20g)
        if goal_lower == 'high-protein':
            threshold = self.target_value if self.target_value else 20.0
            return hasattr(nutritional_info, 'is_high_protein') and nutritional_info.is_high_protein(threshold)
        
        # Low carb goal (< 30g)
        elif goal_lower == 'low-carb':
            threshold = self.target_value if self.target_value else 30.0
            return hasattr(nutritional_info, 'is_low_carb') and nutritional_info.is_low_carb(threshold)
        
        # Low fat goal (< 10g)
        elif goal_lower == 'low-fat':
            threshold = self.target_value if self.target_value else 10.0
            return hasattr(nutritional_info, 'is_low_fat') and nutritional_info.is_low_fat(threshold)
        
        # Low calorie goal (< 400 cal)
        elif goal_lower == 'low-calorie':
            threshold = self.target_value if self.target_value else 400.0
            return hasattr(nutritional_info, 'is_low_calorie') and nutritional_info.is_low_calorie(threshold)
        
        # High fiber goal (>= 5g)
        elif goal_lower == 'high-fiber':
            threshold = self.target_value if self.target_value else 5.0
            return hasattr(nutritional_info, 'is_high_fiber') and nutritional_info.is_high_fiber(threshold)
        
        # Low sodium goal (< 600mg)
        elif goal_lower == 'low-sodium':
            threshold = self.target_value if self.target_value else 600.0
            return hasattr(nutritional_info, 'is_low_sodium') and nutritional_info.is_low_sodium(threshold)
        
        # Low sugar goal
        elif goal_lower in ['low-sugar', 'low-sugars']:
            if hasattr(nutritional_info, 'sugar'):
                threshold = self.target_value if self.target_value else 10.0
                return nutritional_info.sugar < threshold
            return False
        
        # Check if nutritional info has a fits_health_goal method
        elif hasattr(nutritional_info, 'fits_health_goal'):
            return nutritional_info.fits_health_goal(goal_lower)
        
        return False
    
    def get_priority_level(self) -> int:
        """Get numeric priority level (1=low, 2=medium, 3=high)"""
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        return priority_map.get(self.priority.lower(), 2)
    
    def get_goal_description(self) -> str:
        """Get human-readable description of the goal"""
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
    
    def __str__(self) -> str:
        target = f" (target: {self.target_value})" if self.target_value else ""
        return f"{self.get_goal_description()}{target}"
    
    def __repr__(self) -> str:
        return f"HealthGoal(goal_type='{self.goal_type}', priority='{self.priority}')"
