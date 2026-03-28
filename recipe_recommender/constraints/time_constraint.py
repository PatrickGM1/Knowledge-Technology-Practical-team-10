"""
Time constraint model for recipe recommendation system
"""

from dataclasses import dataclass


@dataclass
class TimeConstraint:
    """Represents time constraints for recipe preparation"""
    
    available_minutes: int
    includes_prep: bool = True
    flexibility: bool = False
    
    # Check if a recipe fits the time constraint
    def can_fit(self, recipe) -> bool:
        total_time = self._calculate_recipe_time(recipe)
        
        if total_time is None:
            return True
        
        if not self.flexibility:
            return total_time <= self.available_minutes
        else:
            return total_time <= (self.available_minutes + 10)
    
    # Calculate total time needed for a recipe
    def _calculate_recipe_time(self, recipe) -> int:
        total_time = 0
        
        if hasattr(recipe, 'prep_time') and recipe.prep_time:
            if self.includes_prep:
                total_time += recipe.prep_time
        
        if hasattr(recipe, 'cooking_time'):
            cooking_time = recipe.cooking_time
            
            if hasattr(cooking_time, 'value'):
                cooking_time_str = cooking_time.value.lower()
            else:
                cooking_time_str = str(cooking_time).lower()
            
            time_map = {
                'less than 15': 10,
                'less than 15 minutes': 10,
                '15 to 45': 30,
                '15 to 45 minutes': 30,
                'more than 45': 60,
                'more than 45 minutes': 60
            }
            
            for key, minutes in time_map.items():
                if key in cooking_time_str:
                    total_time += minutes
                    break
        
        elif hasattr(recipe, 'cook_time') and recipe.cook_time:
            total_time += recipe.cook_time
        
        return total_time if total_time > 0 else None
    
    # Get a human-readable description of the time constraint
    def get_time_description(self) -> str:
        if self.available_minutes < 15:
            return "Quick meal (< 15 min)"
        elif self.available_minutes <= 45:
            return f"Moderate time ({self.available_minutes} min)"
        else:
            return f"Extended cooking ({self.available_minutes} min)"
    
    # Check if the available time is for a quick cook
    def is_quick_cook(self) -> bool:
        return self.available_minutes < 20
    
    # User-friendly string for the time constraint
    def __str__(self) -> str:
        flex = " (flexible)" if self.flexibility else ""
        return f"{self.available_minutes} minutes available{flex}"
