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
    

