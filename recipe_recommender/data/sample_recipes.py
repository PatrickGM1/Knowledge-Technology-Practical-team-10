from models import (
    Recipe, Diet, DietRestriction, CookingTime, 
    Skill, CookingMethod, Budget, Meal, Macros
)


# Sample recipes for the recommender system
SAMPLE_RECIPES = [
    Recipe(
        name="Cacio e pepe",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.STUDENT_LIFE,
        meal=Meal.LUNCH,
        macros=[Macros.LOW_FATS]
    ),
    
    Recipe(
        name="Risotto allo zafferano",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET_FRIENDLY,
        meal=Meal.DINNER,
        macros=[Macros.LOW_SUGARS]
    ),
    
    Recipe(
        name="Saltimbocca alla romana",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NUTS_ALLERGIES, DietRestriction.LACTOSE_INTOLERANT, DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN, CookingMethod.OVEN],
        budget=Budget.BUDGET_FRIENDLY,
        meal=Meal.LUNCH,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_CARBS, Macros.LOW_SUGARS]
    ),
    
    Recipe(
        name="Fritta di patate",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.GOURMET,
        meal=Meal.SNACK,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_SUGARS]
    ),
    
    Recipe(
        name="Dark Chocolate Energy Bites",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.GLUTEN_INTOLERANT, DietRestriction.DIABETES],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET_FRIENDLY,
        meal=Meal.SNACK,
        macros=[Macros.LOW_SUGARS, Macros.HIGH_PROTEIN]
    )
]


def get_all_recipes():
    """Return all sample recipes"""
    return SAMPLE_RECIPES


def filter_recipes(preferences):
    """
    Filter recipes based on user preferences
    
    Args:
        preferences: Dictionary with user preferences from the quiz
        
    Returns:
        List of matching Recipe objects
    """
    matching_recipes = []
    
    for recipe in SAMPLE_RECIPES:
        match = True
        
        # Check diet
        if preferences.get('diet') and recipe.diet not in preferences['diet']:
            match = False
        
        # Check dietary restrictions - recipe must accommodate all user restrictions
        if preferences.get('diet_restrictions'):
            for restriction in preferences['diet_restrictions']:
                if restriction != DietRestriction.NONE and restriction not in recipe.diet_restrictions:
                    match = False
                    break
        
        # Check cooking time
        if preferences.get('cooking_time') and recipe.cooking_time not in preferences['cooking_time']:
            match = False
        
        # Check skill level
        if preferences.get('skill') and recipe.skill not in preferences['skill']:
            match = False
        
        # Check cooking methods - recipe must use at least one preferred method
        if preferences.get('cooking_methods'):
            if not any(method in recipe.cooking_methods for method in preferences['cooking_methods']):
                match = False
        
        # Check budget
        if preferences.get('budget') and recipe.budget not in preferences['budget']:
            match = False
        
        # Check meal type
        if preferences.get('meal') and recipe.meal not in preferences['meal']:
            match = False
        
        # Check macros - recipe should have at least one matching macro
        if preferences.get('macros'):
            if not any(macro in recipe.macros for macro in preferences['macros']):
                match = False
        
        if match:
            matching_recipes.append(recipe)
    
    return matching_recipes
