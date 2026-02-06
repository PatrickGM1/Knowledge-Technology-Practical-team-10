"""
Budget constraint domain class for recipe recommendation system.
Represents a user's budget limitations and preferences.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BudgetConstraint:
    """Represents budget constraints for recipe selection"""
    
    min_cost: float = 0.0
    max_cost: float = float('inf')
    preferred_range: str = "moderate"  # budget, moderate, premium
    flexibility: str = "flexible"  # strict, flexible, very_flexible
    
    def __post_init__(self):
        """Set cost ranges based on preferred range if not explicitly set"""
        if self.max_cost == float('inf') and self.min_cost == 0.0:
            ranges = {
                'low_cost': (0.0, 15.0),
                'moderate': (10.0, 30.0),
                'premium': (25.0, float('inf'))
            }
            self.min_cost, self.max_cost = ranges.get(self.preferred_range.lower(), (0.0, float('inf')))
    
    def can_afford(self, recipe) -> bool:
        """
        Check if recipe cost fits within budget constraints.
        
        Args:
            recipe: Recipe object with cost attribute
            
        Returns:
            True if recipe is affordable, False otherwise
        """
        if not hasattr(recipe, 'cost'):
            # If recipe doesn't have cost, check budget enum instead
            if hasattr(recipe, 'budget'):
                return self._check_budget_enum(recipe.budget)
            return True  # If no cost info, assume affordable
        
        recipe_cost = recipe.cost
        
        # Strict: must be within range
        if self.flexibility == "strict":
            return self.min_cost <= recipe_cost <= self.max_cost
        
        # Flexible: allow 20% over budget
        elif self.flexibility == "flexible":
            flexibility_margin = self.max_cost * 0.2
            return self.min_cost <= recipe_cost <= (self.max_cost + flexibility_margin)
        
        # Very flexible: allow 50% over budget
        else:  # very_flexible
            flexibility_margin = self.max_cost * 0.5
            return recipe_cost <= (self.max_cost + flexibility_margin)
    
    def _check_budget_enum(self, recipe_budget) -> bool:
        """Check if recipe's budget enum matches user's preferred range"""
        # Get enum value as string
        budget_value = recipe_budget.value if hasattr(recipe_budget, 'value') else str(recipe_budget)
        budget_lower = budget_value.lower()
        
        # Map budget preferences to acceptable recipe budgets
        acceptable = {
            'budget': ['budget'],
            'moderate': ['budget', 'moderate'],
            'premium': ['moderate', 'premium']
        }
        
        preferred = self.preferred_range.lower()
        return budget_lower in acceptable.get(preferred, ['budget', 'moderate', 'premium'])
    
    def get_cost_range_description(self) -> str:
        """Get human-readable description of cost range"""
        if self.max_cost == float('inf'):
            return f"${self.min_cost:.2f}+"
        return f"${self.min_cost:.2f} - ${self.max_cost:.2f}"
    
    def __str__(self) -> str:
        return f"Budget: {self.preferred_range} ({self.get_cost_range_description()})"
    
    def __repr__(self) -> str:
        return f"BudgetConstraint(preferred_range='{self.preferred_range}', flexibility='{self.flexibility}')"
