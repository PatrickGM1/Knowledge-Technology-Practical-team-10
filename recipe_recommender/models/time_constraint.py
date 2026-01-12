"""
Time constraint domain class for recipe recommendation system.
Represents a user's available cooking time and flexibility.
"""

from dataclasses import dataclass


@dataclass
class TimeConstraint:
    """Represents time constraints for recipe preparation"""
    
    available_minutes: int
    includes_prep: bool = True
    flexibility: bool = False
    
    def can_fit(self, recipe) -> bool:
        """
        Check if recipe's cooking time fits within user's time constraint.
        
        Args:
            recipe: Recipe object with prep_time and/or cooking_time
            
        Returns:
            True if recipe can be completed in available time, False otherwise
        """
        total_time = self._calculate_recipe_time(recipe)
        
        if total_time is None:
            return True  # If no time info, assume it fits
        
        # Strict: must be within available time
        if not self.flexibility:
            return total_time <= self.available_minutes
        
        # Flexible: allow 10 minutes extra
        else:
            return total_time <= (self.available_minutes + 10)
    
    def _calculate_recipe_time(self, recipe) -> int:
        """Calculate total time needed for recipe"""
        total_time = 0
        
        # Try to get prep_time attribute
        if hasattr(recipe, 'prep_time') and recipe.prep_time:
            if self.includes_prep:
                total_time += recipe.prep_time
        
        # Try to get cooking_time enum and convert to minutes
        if hasattr(recipe, 'cooking_time'):
            cooking_time = recipe.cooking_time
            
            # If it's an enum, get the value
            if hasattr(cooking_time, 'value'):
                cooking_time_str = cooking_time.value.lower()
            else:
                cooking_time_str = str(cooking_time).lower()
            
            # Map cooking time categories to average minutes
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
        
        # Try to get cook_time attribute
        elif hasattr(recipe, 'cook_time') and recipe.cook_time:
            total_time += recipe.cook_time
        
        return total_time if total_time > 0 else None
    
    def get_time_description(self) -> str:
        """Get human-readable description of time constraint"""
        if self.available_minutes < 15:
            return "Quick meal (< 15 min)"
        elif self.available_minutes <= 45:
            return f"Moderate time ({self.available_minutes} min)"
        else:
            return f"Extended cooking ({self.available_minutes} min)"
    
    def is_quick_cook(self) -> bool:
        """Check if this is a quick cooking constraint (< 20 minutes)"""
        return self.available_minutes < 20
    
    def __str__(self) -> str:
        flex = " (flexible)" if self.flexibility else ""
        return f"{self.available_minutes} minutes available{flex}"
    
    def __repr__(self) -> str:
        return f"TimeConstraint(available_minutes={self.available_minutes}, flexibility={self.flexibility})"
