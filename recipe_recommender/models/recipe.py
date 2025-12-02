from enum import Enum
from typing import List, Optional


class Diet(Enum):
    """Diet types"""
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    PESCATARIAN = "pescatarian"
    OMNIVORE = "omnivore"


class DietRestriction(Enum):
    """Dietary restrictions"""
    LACTOSE_INTOLERANT = "lactose intolerant"
    GLUTEN_INTOLERANT = "gluten intolerant"
    NUTS_ALLERGIES = "nuts allergies"
    DIABETES = "diabetes"
    NONE = "none"


class CookingTime(Enum):
    """Cooking time categories"""
    LESS_THAN_15 = "less than 15 minutes"
    BETWEEN_15_45 = "15 to 45 minutes"
    MORE_THAN_45 = "more than 45 minutes"   


class Skill(Enum):
    """Cooking skill levels"""
    EASY = "easy"
    MEDIUM = "medium"
    EXPERIENCED = "experienced"


class CookingMethod(Enum):
    """Cooking methods"""
    PAN = "pan"
    OVEN = "oven"
    GRILL = "grill"


class Budget(Enum):
    """Budget categories"""
    STUDENT_LIFE = "student life"
    BUDGET_FRIENDLY = "budget friendly"
    GOURMET = "gourmet"


class Meal(Enum):
    """Meal types"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"


class Macros(Enum):
    """Macronutrient profiles"""
    HIGH_PROTEIN = "high in protein"
    LOW_FATS = "low fats"
    LOW_CARBS = "low carbs"
    LOW_SUGARS = "low sugars"


class Recipe:
    """
    Recipe class representing a cooking recipe with various attributes
    for categorization and filtering.
    """
    
    def __init__(
        self,
        name: str,
        diet: Diet,
        diet_restrictions: List[DietRestriction],
        cooking_time: CookingTime,
        skill: Skill,
        cooking_methods: List[CookingMethod],
        budget: Budget,
        meal: Meal,
        macros: List[Macros]
    ):
        """
        Initialize a Recipe instance.
        
        Args:
            name: Name of the recipe
            diet: Diet type (vegan, vegetarian, pescatarian, omnivore)
            diet_restrictions: List of dietary restrictions the recipe accommodates
            cooking_time: Time required to cook
            skill: Required cooking skill level
            cooking_methods: List of cooking methods used
            budget: Budget category
            meal: Meal type
            macros: List of macronutrient profiles
        """
        self.name = name
        self.diet = diet
        self.diet_restrictions = diet_restrictions
        self.cooking_time = cooking_time
        self.skill = skill
        self.cooking_methods = cooking_methods
        self.budget = budget
        self.meal = meal
        self.macros = macros
    
    def __repr__(self) -> str:
        return f"Recipe(name='{self.name}', diet={self.diet.value}, meal={self.meal.value})"
    
    def __str__(self) -> str:
        return f"{self.name} - {self.diet.value} {self.meal.value}"
    
    def matches_diet(self, diet: Diet) -> bool:
        """Check if recipe matches a specific diet type."""
        return self.diet == diet
    
    def matches_restriction(self, restriction: DietRestriction) -> bool:
        """Check if recipe accommodates a specific dietary restriction."""
        return restriction in self.diet_restrictions
    
    def matches_cooking_time(self, cooking_time: CookingTime) -> bool:
        """Check if recipe matches cooking time requirement."""
        return self.cooking_time == cooking_time
    
    def matches_skill(self, skill: Skill) -> bool:
        """Check if recipe matches skill level."""
        return self.skill == skill
    
    def matches_cooking_method(self, method: CookingMethod) -> bool:
        """Check if recipe uses a specific cooking method."""
        return method in self.cooking_methods
    
    def matches_budget(self, budget: Budget) -> bool:
        """Check if recipe matches budget category."""
        return self.budget == budget
    
    def matches_meal(self, meal: Meal) -> bool:
        """Check if recipe is for a specific meal type."""
        return self.meal == meal
    
    def matches_macro(self, macro: Macros) -> bool:
        """Check if recipe has a specific macro profile."""
        return macro in self.macros
    
    def to_dict(self) -> dict:
        """Convert recipe to dictionary representation."""
        return {
            'name': self.name,
            'diet': self.diet.value,
            'diet_restrictions': [dr.value for dr in self.diet_restrictions],
            'cooking_time': self.cooking_time.value,
            'skill': self.skill.value,
            'cooking_methods': [cm.value for cm in self.cooking_methods],
            'budget': self.budget.value,
            'meal': self.meal.value,
            'macros': [m.value for m in self.macros]
        }
