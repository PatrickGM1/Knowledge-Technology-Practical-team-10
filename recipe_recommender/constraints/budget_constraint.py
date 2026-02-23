"""
Budget constraint model for recipe recommendation system
"""

from dataclasses import dataclass


@dataclass
class BudgetConstraint:
    """Represents budget constraints for recipe selection"""
    
    min_cost: float = 0.0
    max_cost: float = float('inf')
    preferred_range: str = "moderate"
    flexibility: str = "flexible"
    
    def __post_init__(self):
        if self.max_cost == float('inf') and self.min_cost == 0.0:
            ranges = {
                'low_cost': (0.0, 15.0),
                'moderate': (10.0, 30.0),
                'premium': (25.0, float('inf'))
            }
            self.min_cost, self.max_cost = ranges.get(self.preferred_range.lower(), (0.0, float('inf')))
    
    def can_afford(self, recipe) -> bool:
        if not hasattr(recipe, 'cost'):
            if hasattr(recipe, 'budget'):
                return self._check_budget_enum(recipe.budget)
            return True
        
        recipe_cost = recipe.cost
        
        if self.flexibility == "strict":
            return self.min_cost <= recipe_cost <= self.max_cost
        elif self.flexibility == "flexible":
            flexibility_margin = self.max_cost * 0.2
            return self.min_cost <= recipe_cost <= (self.max_cost + flexibility_margin)
        else:
            flexibility_margin = self.max_cost * 0.5
            return recipe_cost <= (self.max_cost + flexibility_margin)
    
    def _check_budget_enum(self, recipe_budget) -> bool:
        budget_value = recipe_budget.value if hasattr(recipe_budget, 'value') else str(recipe_budget)
        budget_lower = budget_value.lower()
        
        acceptable = {
            'budget': ['budget'],
            'moderate': ['budget', 'moderate'],
            'premium': ['moderate', 'premium']
        }
        
        preferred = self.preferred_range.lower()
        return budget_lower in acceptable.get(preferred, ['budget', 'moderate', 'premium'])
    
    def get_cost_range_description(self) -> str:
        if self.max_cost == float('inf'):
            return f"${self.min_cost:.2f}+"
        return f"${self.min_cost:.2f} - ${self.max_cost:.2f}"
    
    def __str__(self) -> str:
        return f"Budget: {self.preferred_range} ({self.get_cost_range_description()})"
