from models import (
    Recipe, Diet, DietRestriction, CookingTime, 
    Skill, CookingMethod, Budget, Meal, Macros,
    Ingredient, Equipment, NutritionalInfo, DetailedCookingMethod
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
        budget=Budget.LOW_COST,
        meal=Meal.LUNCH,
        macros=[Macros.LOW_FATS],
        ingredients=[
            Ingredient(name="pasta", quantity=200, unit="g", category="grain"),
            Ingredient(name="pecorino cheese", quantity=50, unit="g", category="dairy", allergens=["dairy"]),
            Ingredient(name="black pepper", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="salt", quantity=1, unit="tsp", category="spice", is_optional=True),
        ],
        equipment=[
            Equipment(name="pot", category="cookware"),
            Equipment(name="pan", category="cookware"),
            Equipment(name="grater", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=450,
            protein=18,
            carbohydrates=65,
            fat=12,
            fiber=3,
            sodium=400
        ),
        instructions=[
            "Boil salted water and cook pasta until al dente",
            "Reserve 1 cup of pasta water before draining",
            "Grate pecorino cheese finely",
            "Toast black pepper in a pan",
            "Add cooked pasta and pasta water to pan",
            "Toss with cheese and pepper until creamy",
            "Serve immediately"
        ],
        servings=2,
        prep_time=5,
        cuisine="Italian",
        description="Classic Roman pasta dish with cheese and black pepper",
        cost=3.5  # Budget-friendly
    ),
    
    Recipe(
        name="Risotto allo zafferano",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[Macros.LOW_SUGARS],
        ingredients=[
            Ingredient(name="arborio rice", quantity=300, unit="g", category="grain"),
            Ingredient(name="vegetable broth", quantity=1, unit="liter", category="other"),
            Ingredient(name="onion", quantity=1, unit="piece", category="vegetable", preparation="finely chopped"),
            Ingredient(name="white wine", quantity=100, unit="ml", category="other", is_optional=True),
            Ingredient(name="saffron", quantity=0.5, unit="g", category="spice"),
            Ingredient(name="butter", quantity=30, unit="g", category="dairy", allergens=["dairy"]),
            Ingredient(name="parmesan cheese", quantity=50, unit="g", category="dairy", allergens=["dairy"]),
        ],
        equipment=[
            Equipment(name="large pan", category="cookware"),
            Equipment(name="wooden spoon", category="utensil"),
            Equipment(name="ladle", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=520,
            protein=14,
            carbohydrates=75,
            fat=16,
            fiber=2,
            sodium=600
        ),
        instructions=[
            "Heat broth and keep it warm",
            "Sauté onion in butter until translucent",
            "Add rice and toast for 2 minutes",
            "Add wine and let it evaporate",
            "Add broth one ladle at a time, stirring constantly",
            "After 15 minutes, add saffron",
            "Continue cooking until rice is creamy (about 18-20 minutes total)",
            "Stir in butter and parmesan",
            "Let rest for 2 minutes before serving"
        ],
        servings=4,
        prep_time=10,
        cuisine="Italian",
        description="Creamy saffron risotto from Milan",
        cost=6.5  # Moderate due to saffron
    ),
    
    Recipe(
        name="Saltimbocca alla romana",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NUTS_ALLERGIES, DietRestriction.LACTOSE_INTOLERANT, DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN, CookingMethod.OVEN],
        budget=Budget.MODERATE,
        meal=Meal.LUNCH,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_CARBS, Macros.LOW_SUGARS],
        ingredients=[
            Ingredient(name="veal cutlets", quantity=4, unit="pieces", category="protein"),
            Ingredient(name="prosciutto", quantity=4, unit="slices", category="protein"),
            Ingredient(name="sage leaves", quantity=8, unit="pieces", category="spice"),
            Ingredient(name="white wine", quantity=100, unit="ml", category="other"),
            Ingredient(name="butter", quantity=30, unit="g", category="dairy", allergens=["dairy"], 
                      substitutes={"olive oil": 1.0}),
            Ingredient(name="flour", quantity=2, unit="tbsp", category="grain", is_optional=True),
        ],
        equipment=[
            Equipment(name="pan", category="cookware"),
            Equipment(name="tongs", category="utensil"),
            Equipment(name="toothpicks", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=320,
            protein=35,
            carbohydrates=5,
            fat=15,
            fiber=0.5,
            sodium=550
        ),
        instructions=[
            "Pound veal cutlets to even thickness",
            "Place prosciutto and sage on each cutlet, secure with toothpick",
            "Dust lightly with flour if using",
            "Heat butter in pan over medium-high heat",
            "Cook cutlets sage-side down for 2-3 minutes",
            "Flip and cook for another 2 minutes",
            "Remove cutlets and keep warm",
            "Deglaze pan with white wine",
            "Pour sauce over cutlets and serve"
        ],
        servings=4,
        prep_time=10,
        cuisine="Italian",
        description="Roman veal cutlets with prosciutto and sage",
        cost=5.5  # Moderate with veal and prosciutto
    ),
    
    Recipe(
        name="Fritta di patate",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.PREMIUM,
        meal=Meal.SNACK,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_SUGARS],
        ingredients=[
            Ingredient(name="potatoes", quantity=500, unit="g", category="vegetable", preparation="thinly sliced"),
            Ingredient(name="eggs", quantity=6, unit="pieces", category="protein", allergens=["eggs"]),
            Ingredient(name="onion", quantity=1, unit="piece", category="vegetable", preparation="sliced", is_optional=True),
            Ingredient(name="olive oil", quantity=3, unit="tbsp", category="oil"),
            Ingredient(name="salt", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="pepper", quantity=0.5, unit="tsp", category="spice"),
        ],
        equipment=[
            Equipment(name="large pan", category="cookware"),
            Equipment(name="spatula", category="utensil"),
            Equipment(name="bowl", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=280,
            protein=14,
            carbohydrates=25,
            fat=14,
            fiber=3,
            sodium=420
        ),
        instructions=[
            "Heat olive oil in pan",
            "Fry potato slices until golden and tender",
            "Beat eggs with salt and pepper",
            "Add cooked potatoes to eggs",
            "Pour mixture back into pan",
            "Cook until bottom is set",
            "Flip and cook other side until golden",
            "Serve hot or at room temperature"
        ],
        servings=4,
        prep_time=8,
        cuisine="Italian",
        description="Italian potato frittata",
        cost=9.0  # Premium category
    ),
    
    Recipe(
        name="Dark Chocolate Energy Bites",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.GLUTEN_INTOLERANT, DietRestriction.DIABETES],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.MODERATE,
        meal=Meal.SNACK,
        macros=[Macros.LOW_SUGARS, Macros.HIGH_PROTEIN],
        ingredients=[
            Ingredient(name="rolled oats", quantity=200, unit="g", category="grain", dietary_flags=["gluten-free"]),
            Ingredient(name="dark chocolate", quantity=100, unit="g", category="sweetener"),
            Ingredient(name="almond butter", quantity=100, unit="g", category="protein", allergens=["nuts"],
                      substitutes={"sunflower seed butter": 1.0, "peanut butter": 1.0}),
            Ingredient(name="honey", quantity=3, unit="tbsp", category="sweetener",
                      substitutes={"maple syrup": 1.0, "agave": 1.0}),
            Ingredient(name="chia seeds", quantity=2, unit="tbsp", category="other", is_optional=True),
            Ingredient(name="vanilla extract", quantity=1, unit="tsp", category="spice"),
        ],
        equipment=[
            Equipment(name="bowl", category="utensil"),
            Equipment(name="spoon", category="utensil"),
            Equipment(name="baking sheet", category="bakeware", alternatives=["plate"]),
        ],
        nutritional_info=NutritionalInfo(
            calories=180,
            protein=6,
            carbohydrates=20,
            fat=9,
            fiber=4,
            sodium=25,
            sugar=8
        ),
        instructions=[
            "Mix all ingredients in a bowl",
            "Let mixture chill in refrigerator for 30 minutes",
            "Roll into bite-sized balls",
            "Store in refrigerator for up to 1 week"
        ],
        servings=12,
        prep_time=10,
        cuisine="American",
        description="Healthy no-bake energy bites with dark chocolate",
        cost=4.5  # Moderate with specialty ingredients
    ),

    # 1) Trout fillet marinated in sugar (snack)
    Recipe(
        name="Trout Fillet Marinated in Sugar",
        diet=Diet.PESCATARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.MARINATED],
        budget=Budget.MODERATE,
        meal=Meal.SNACK,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_CARBS],
        ingredients=[
            Ingredient(name="trout fillet", quantity=250, unit="g", category="protein", preparation="skin removed"),
            Ingredient(name="sugar", quantity=1, unit="tbsp", category="sweetener"),
            Ingredient(name="salt", quantity=1, unit="tsp", category="spice"),
        ],
        equipment=[
            Equipment(name="bowl", category="utensil"),
            Equipment(name="sealed container", category="utensil", alternatives=["plate"]),
        ],
        nutritional_info=NutritionalInfo(
            calories=280,
            protein=42,
            carbohydrates=4,
            fat=10,
            fiber=0,
            sodium=600,
            sugar=4
        ),
        instructions=[
            "Use a cleaned trout fillet with skin removed",
            "Rub the trout fillet with sugar and salt",
            "Place the fillet in a sealed container",
            "Marinate in the refrigerator for 2–3 hours",
            "Ready to eat"
        ],
        servings=2,
        prep_time=5,
        cuisine="Romanian-inspired",
        description="Snack: trout fillet marinated with sugar and salt for 2–3 hours, ready to eat",
        cost=5.0
    ),

    # 2) American-style pico de gallo salad
    Recipe(
        name="American-Style Pico de Gallo Salad",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.BOWL],
        budget=Budget.LOW_COST,
        meal=Meal.LUNCH,
        macros=[Macros.LOW_SUGARS, Macros.LOW_FATS],
        ingredients=[
            Ingredient(name="tomatoes", quantity=2, unit="pieces", category="vegetable"),
            Ingredient(name="red onion", quantity=0.5, unit="piece", category="vegetable"),
            Ingredient(name="jalapeno", quantity=1, unit="piece", category="vegetable", is_optional=True),
            Ingredient(name="lemon juice", quantity=1, unit="tbsp", category="other"),
            Ingredient(name="salt", quantity=0.5, unit="tsp", category="spice"),
            Ingredient(name="black pepper", quantity=0.5, unit="tsp", category="spice"),
        ],
        equipment=[
            Equipment(name="knife", category="utensil"),
            Equipment(name="bowl", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=70,
            protein=2,
            carbohydrates=14,
            fat=0.5,
            fiber=3,
            sodium=250,
            sugar=7
        ),
        instructions=[
            "Dice the tomatoes",
            "Finely chop the red onion",
            "Chop the jalapeno if using",
            "Mix with lemon juice, salt, and black pepper to taste",
            "Serve immediately"
        ],
        servings=2,
        prep_time=10,
        cuisine="American",
        description="Fresh American-style pico de gallo made with tomatoes, red onion, optional jalapeno, lemon juice, salt, and pepper",
        cost=2.0
    ),

    # 3) Flatbread taco with minced beef and red onion
    Recipe(
        name="Flatbread Taco with Minced Beef and Red Onion",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN, CookingMethod.OVEN],
        budget=Budget.LOW_COST,
        meal=Meal.SNACK,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_SUGARS],
        ingredients=[
            Ingredient(name="flatbread", quantity=2, unit="pieces", category="grain"),
            Ingredient(name="ground beef", quantity=250, unit="g", category="protein"),
            Ingredient(name="red onion", quantity=1, unit="piece", category="vegetable", preparation="julienned"),
            Ingredient(name="salt", quantity=0.5, unit="tsp", category="spice"),
            Ingredient(name="black pepper", quantity=0.5, unit="tsp", category="spice"),
            Ingredient(name="mixed spices", quantity=1, unit="tbsp", category="spice", is_optional=True),
            Ingredient(name="seasoning", quantity=1, unit="tsp", category="spice", is_optional=True),
        ],
        equipment=[
            Equipment(name="baking tray", category="bakeware", alternatives=["pan"]),
            Equipment(name="knife", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=520,
            protein=33,
            carbohydrates=45,
            fat=22,
            fiber=4,
            sodium=650,
            sugar=3
        ),
        instructions=[
            "Spread the ground beef evenly over the flatbread",
            "Add julienned red onion on top",
            "Season with salt and black pepper",
            "Add mixed spices and optional seasoning",
            "Bake until the meat is fully cooked",
            "Serve hot"
        ],
        servings=2,
        prep_time=7,
        cuisine="Mexican-inspired",
        description="Quick flatbread taco with evenly spread minced beef, red onion, salt, pepper, and spices",
        cost=4.0
    ),

    # 4) Cessar-style chicken salad
    Recipe(
        name="Cessar Chicken Salad",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.BOWL, CookingMethod.PAN],
        budget=Budget.MODERATE,
        meal=Meal.LUNCH,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_SUGARS],
        ingredients=[
            Ingredient(name="green lettuce", quantity=150, unit="g", category="vegetable"),
            Ingredient(name="chicken breast", quantity=200, unit="g", category="protein", preparation="pan-cooked"),
            Ingredient(name="cherry tomatoes", quantity=150, unit="g", category="vegetable"),
            Ingredient(name="boiled egg", quantity=1, unit="piece", category="protein", allergens=["eggs"]),
            Ingredient(name="parmesan cheese", quantity=25, unit="g", category="dairy", allergens=["dairy"]),
            Ingredient(name="croutons", quantity=30, unit="g", category="grain"),
            Ingredient(name="mayonnaise sauce", quantity=2, unit="tbsp", category="other"),
        ],
        equipment=[
            Equipment(name="pan", category="cookware"),
            Equipment(name="bowl", category="utensil"),
            Equipment(name="knife", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=520,
            protein=40,
            carbohydrates=20,
            fat=30,
            fiber=4,
            sodium=700,
            sugar=5
        ),
        instructions=[
            "Cook the chicken breast in a pan according to preference",
            "Assemble the salad with lettuce, chicken, cherry tomatoes, boiled egg, parmesan, croutons, and mayonnaise sauce"
        ],
        servings=1,
        prep_time=10,
        cuisine="International",
        description="Chicken salad with lettuce, pan-cooked chicken, cherry tomatoes, boiled egg, parmesan, croutons, and mayonnaise sauce",
        cost=6.0
    ),

    # 5) Meal replacement protein shake
    Recipe(
        name="Meal Replacement Protein Shake",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NUTS_ALLERGIES, DietRestriction.LACTOSE_INTOLERANT],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.BLENDER],
        budget=Budget.LOW_COST,
        meal=Meal.SNACK,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_SUGARS],
        ingredients=[
            Ingredient(name="milk", quantity=300, unit="ml", category="dairy", allergens=["dairy"],
                      substitutes={"almond milk": 1.0, "soy milk": 1.0, "oat milk": 1.0}),
            Ingredient(name="protein powder", quantity=30, unit="g", category="protein"),
            Ingredient(name="rolled oats", quantity=30, unit="g", category="grain"),
            Ingredient(
                name="peanut butter",
                quantity=1,
                unit="tbsp",
                category="protein",
                allergens=["nuts"],
                substitutes={"sunflower seed butter": 1.0}
            ),
            Ingredient(name="banana", quantity=1, unit="piece", category="fruit"),
            Ingredient(
                name="flavoring",
                quantity=1,
                unit="tsp",
                category="other",
                is_optional=True,
                substitutes={"honey": 1.0, "maple syrup": 1.0}
            ),
        ],
        equipment=[
            Equipment(name="blender", category="appliance"),
        ],
        nutritional_info=NutritionalInfo(
            calories=480,
            protein=35,
            carbohydrates=58,
            fat=14,
            fiber=7,
            sodium=220,
            sugar=12
        ),
        instructions=[
            "Add all ingredients to the blender",
            "Blend until smooth",
            "Serve immediately"
        ],
        servings=1,
        prep_time=5,
        cuisine="International",
        description="High-protein meal replacement shake made with milk, protein powder, oats, peanut butter, banana, and optional flavoring",
        cost=3.5
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
