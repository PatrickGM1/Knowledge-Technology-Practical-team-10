from enum import Enum
from typing import List, Optional, Dict
from .ingredient import Ingredient
from .equipment import Equipment
from .nutritional_info import NutritionalInfo
from .cooking_method import CookingMethod as DetailedCookingMethod


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
    BUDGET = "budget"
    MODERATE = "moderate"
    PREMIUM = "premium"


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
    
    Enhanced with ingredients, equipment, nutritional info, and detailed cooking methods.
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
        macros: List[Macros],
        ingredients: Optional[List[Ingredient]] = None,
        equipment: Optional[List[Equipment]] = None,
        detailed_cooking_methods: Optional[List[DetailedCookingMethod]] = None,
        nutritional_info: Optional[NutritionalInfo] = None,
        instructions: Optional[List[str]] = None,
        servings: int = 4,
        prep_time: Optional[int] = None,  # in minutes
        cuisine: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize a Recipe instance.
        
        Args:
            name: Name of the recipe
            diet: Diet type (vegan, vegetarian, pescatarian, omnivore)
            diet_restrictions: List of dietary restrictions the recipe accommodates
            cooking_time: Time required to cook
            skill: Required cooking skill level
            cooking_methods: List of cooking methods used (enum)
            budget: Budget category
            meal: Meal type
            macros: List of macronutrient profiles
            ingredients: List of Ingredient objects
            equipment: List of Equipment objects needed
            detailed_cooking_methods: List of detailed CookingMethod objects
            nutritional_info: NutritionalInfo object
            instructions: Step-by-step cooking instructions
            servings: Number of servings the recipe yields
            prep_time: Preparation time in minutes
            cuisine: Cuisine type (e.g., 'Italian', 'Asian', 'Mexican')
            description: Recipe description
            tags: Additional tags for categorization
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
        
        # Enhanced attributes
        self.ingredients = ingredients or []
        self.equipment = equipment or []
        self.detailed_cooking_methods = detailed_cooking_methods or []
        self.nutritional_info = nutritional_info or NutritionalInfo()
        self.instructions = instructions or []
        self.servings = servings
        self.prep_time = prep_time
        self.cuisine = cuisine
        self.description = description
        self.tags = tags or []
    
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
    
    def has_ingredient(self, ingredient_name: str) -> bool:
        """Check if recipe contains a specific ingredient."""
        return any(ing.name.lower() == ingredient_name.lower() for ing in self.ingredients)
    
    def requires_equipment(self, equipment_name: str) -> bool:
        """Check if recipe requires specific equipment."""
        return any(eq.name.lower() == equipment_name.lower() for eq in self.equipment)
    
    def uses_cooking_method(self, method_name: str) -> bool:
        """Check if recipe uses a specific detailed cooking method."""
        return any(cm.name.lower() == method_name.lower() for cm in self.detailed_cooking_methods)
    
    def is_suitable_for_user(self, user) -> bool:
        """
        Check if recipe is suitable for a user based on their profile.
        
        Args:
            user: User object with preferences and restrictions
            
        Returns:
            bool: True if recipe is suitable, False otherwise
        """
        # Check allergies
        for ingredient in self.ingredients:
            for allergen in ingredient.allergens:
                if user.is_allergic_to(allergen):
                    return False
        
        # Check disliked ingredients
        for ingredient in self.ingredients:
            if user.dislikes_ingredient(ingredient.name):
                return False
        
        # Check dietary restrictions (vegan, vegetarian, etc.)
        diet_map = {
            'vegan': Diet.VEGAN,
            'vegetarian': Diet.VEGETARIAN,
            'pescatarian': Diet.PESCATARIAN
        }
        for restriction in user.dietary_restrictions:
            required_diet = diet_map.get(restriction.lower())
            if required_diet and self.diet != required_diet:
                # Check if current diet is compatible
                diet_hierarchy = {
                    Diet.VEGAN: [Diet.VEGAN],
                    Diet.VEGETARIAN: [Diet.VEGAN, Diet.VEGETARIAN],
                    Diet.PESCATARIAN: [Diet.VEGAN, Diet.VEGETARIAN, Diet.PESCATARIAN],
                    Diet.OMNIVORE: [Diet.VEGAN, Diet.VEGETARIAN, Diet.PESCATARIAN, Diet.OMNIVORE]
                }
                if self.diet not in diet_hierarchy.get(required_diet, []):
                    return False
        
        # Check skill level
        if not user.can_cook_complexity(self.skill.value):
            return False
        
        # Check cooking time
        if self.prep_time and not user.within_time_constraint(self.prep_time):
            return False
        
        # Check equipment
        for equip in self.equipment:
            if equip.is_essential and not user.has_equipment(equip.name):
                # Check if user has alternative equipment
                has_alternative = False
                for alt in equip.alternatives:
                    if user.has_equipment(alt):
                        has_alternative = True
                        break
                if not has_alternative:
                    return False
        
        # Check cuisine preference
        if self.cuisine and not user.prefers_cuisine(self.cuisine):
            return False
        
        # Check nutritional goals
        for goal in user.health_goals:
            if not self.nutritional_info.fits_health_goal(goal):
                return False
        
        return True
    
    def get_alternative_ingredients(self, ingredient_name: str) -> List[str]:
        """Get list of substitute ingredients for a specific ingredient."""
        for ingredient in self.ingredients:
            if ingredient.name.lower() == ingredient_name.lower():
                return list(ingredient.substitutes.keys())
        return []
    
    def scale_recipe(self, new_servings: int) -> 'Recipe':
        """
        Create a new Recipe with scaled ingredients and nutritional info.
        
        Args:
            new_servings: New number of servings
            
        Returns:
            Recipe: New recipe with scaled quantities
        """
        scaled_ingredients = [ing.convert_quantity(new_servings, self.servings) for ing in self.ingredients]
        scaled_nutrition = self.nutritional_info.scale_for_servings(new_servings, self.servings)
        
        return Recipe(
            name=self.name,
            diet=self.diet,
            diet_restrictions=self.diet_restrictions,
            cooking_time=self.cooking_time,
            skill=self.skill,
            cooking_methods=self.cooking_methods,
            budget=self.budget,
            meal=self.meal,
            macros=self.macros,
            ingredients=scaled_ingredients,
            equipment=self.equipment.copy(),
            detailed_cooking_methods=self.detailed_cooking_methods.copy(),
            nutritional_info=scaled_nutrition,
            instructions=self.instructions.copy(),
            servings=new_servings,
            prep_time=self.prep_time,
            cuisine=self.cuisine,
            description=self.description,
            tags=self.tags.copy()
        )
    
    def get_total_time(self) -> Optional[int]:
        """Get total time (prep + cooking) in minutes."""
        if self.prep_time:
            # Estimate cooking time from enum
            cooking_time_map = {
                CookingTime.LESS_THAN_15: 15,
                CookingTime.BETWEEN_15_45: 30,
                CookingTime.MORE_THAN_45: 60
            }
            cook_time = cooking_time_map.get(self.cooking_time, 30)
            return self.prep_time + cook_time
        return None
    
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
            'macros': [m.value for m in self.macros],
            'ingredients': [str(ing) for ing in self.ingredients],
            'equipment': [str(eq) for eq in self.equipment],
            'detailed_cooking_methods': [str(cm) for cm in self.detailed_cooking_methods],
            'nutritional_info': str(self.nutritional_info),
            'instructions': self.instructions,
            'servings': self.servings,
            'prep_time': self.prep_time,
            'cuisine': self.cuisine,
            'description': self.description,
            'tags': self.tags
        }
