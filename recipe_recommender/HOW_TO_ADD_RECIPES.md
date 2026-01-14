# How to Add Recipes to the System

## Overview
We currently have **5 recipes** and need **25 total recipes**. You need to add **20 more recipes** to the system.

## File Location
**Edit this file:** `recipe_recommender/data/sample_recipes.py`

## Where to Add Recipes

1. Open `sample_recipes.py`
2. Find the `SAMPLE_RECIPES = [...]` list (starts at line 8)
3. The list currently ends around line 250 with `]`
4. Add new recipes **before** the closing `]` bracket
5. Make sure to add a **comma** after each recipe

## Recipe Template

Copy and paste this template for each new recipe:

```python
    Recipe(
        name="Your Recipe Name",
        diet=Diet.VEGAN,  # Options: VEGAN, VEGETARIAN, PESCATARIAN, OMNIVORE
        diet_restrictions=[DietRestriction.NONE],  # Options: NONE, LACTOSE_INTOLERANT, GLUTEN_INTOLERANT, NUTS_ALLERGIES, DIABETES
        cooking_time=CookingTime.LESS_THAN_15,  # Options: LESS_THAN_15, BETWEEN_15_45, MORE_THAN_45
        skill=Skill.EASY,  # Options: EASY, MEDIUM, EXPERIENCED
        cooking_methods=[CookingMethod.PAN],  # Options: PAN, OVEN, GRILL (can have multiple)
        budget=Budget.LOW_COST,  # Options: LOW_COST, MODERATE, PREMIUM
        meal=Meal.LUNCH,  # Options: BREAKFAST, LUNCH, DINNER, SNACK, DESSERT
        macros=[Macros.HIGH_PROTEIN],  # Options: HIGH_PROTEIN, LOW_FATS, LOW_CARBS, LOW_SUGARS (can have multiple)
        ingredients=[
            Ingredient(name="ingredient1", quantity=100, unit="g", category="protein"),
            Ingredient(name="ingredient2", quantity=2, unit="tbsp", category="spice"),
            # Add more ingredients as needed
        ],
        equipment=[
            Equipment(name="oven", category="cookware"),
            Equipment(name="bowl", category="utensil"),
            # Add more equipment as needed
        ],
        nutritional_info=NutritionalInfo(
            calories=400,
            protein=20,
            carbohydrates=50,
            fat=15,
            fiber=5,
            sodium=300
        ),
        instructions=[
            "Step 1: First instruction",
            "Step 2: Second instruction",
            "Step 3: Third instruction",
            # Add more steps as needed
        ],
        servings=4,
        prep_time=10,  # in minutes
        cuisine="Italian",  # e.g., Italian, French, Mexican, Asian, American
        description="Brief description of your recipe",
        cost=5.0  # Cost per serving in euros
    ),
```

## ⚠️ CRITICAL: Allergen Handling

**The system filters recipes based on allergies!** You MUST add `allergens=[]` to ingredients containing:

### Common Allergens to Flag:

| Allergen | Ingredients to Flag | Example |
|----------|-------------------|---------|
| **Eggs** | eggs, egg whites, egg yolks | `Ingredient(name="eggs", quantity=2, unit="pieces", allergens=["eggs"])` |
| **Dairy** | milk, cheese, butter, cream, yogurt, parmesan, pecorino, mozzarella | `Ingredient(name="butter", quantity=50, unit="g", allergens=["dairy"])` |
| **Tree Nuts** | almonds, walnuts, cashews, almond butter, pecans, hazelnuts | `Ingredient(name="almond butter", quantity=100, unit="g", allergens=["tree nuts"])` |
| **Peanuts** | peanuts, peanut butter | `Ingredient(name="peanuts", quantity=50, unit="g", allergens=["peanuts"])` |
| **Shellfish** | shrimp, crab, lobster, clams, mussels | `Ingredient(name="shrimp", quantity=200, unit="g", allergens=["shellfish"])` |
| **Fish** | salmon, tuna, cod, any fish | `Ingredient(name="salmon", quantity=200, unit="g", allergens=["fish"])` |
| **Wheat** | Use ingredient names: "pasta", "flour", "bread" | `Ingredient(name="pasta", quantity=200, unit="g", category="grain")` |
| **Soy** | tofu, soy sauce, edamame | `Ingredient(name="tofu", quantity=200, unit="g", allergens=["soy"])` |
| **Sesame** | sesame seeds, tahini, sesame oil | `Ingredient(name="tahini", quantity=2, unit="tbsp", allergens=["sesame"])` |

### Allergen Example:
```python
ingredients=[
    Ingredient(name="chicken breast", quantity=400, unit="g", category="protein"),
    Ingredient(name="eggs", quantity=2, unit="pieces", category="protein", allergens=["eggs"]),
    Ingredient(name="parmesan cheese", quantity=50, unit="g", category="dairy", allergens=["dairy"]),
    Ingredient(name="almond butter", quantity=100, unit="g", category="nut", allergens=["tree nuts"]),
],
```

## Ingredient Categories

Use these categories for ingredients:
- `"protein"` - meat, fish, eggs, tofu
- `"vegetable"` - all vegetables
- `"grain"` - pasta, rice, bread
- `"dairy"` - milk, cheese, yogurt
- `"spice"` - spices, herbs, seasonings
- `"oil"` - olive oil, vegetable oil
- `"liquid"` - broth, stock, water
- `"nut"` - nuts and nut butters

## Equipment Categories

Use these categories for equipment:
- `"cookware"` - pots, pans, baking sheets
- `"utensil"` - spatula, whisk, grater
- `"appliance"` - blender, food processor, mixer

## Units

Common units to use:
- Weight: `"g"`, `"kg"`
- Volume: `"ml"`, `"l"`, `"cup"`, `"tbsp"`, `"tsp"`
- Count: `"pieces"`, `"cloves"`, `"slices"`

## Complete Example Recipe

Here's a complete recipe you can use as reference:

```python
    Recipe(
        name="Grilled Chicken Salad",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.GRILL, CookingMethod.PAN],
        budget=Budget.MODERATE,
        meal=Meal.LUNCH,
        macros=[Macros.HIGH_PROTEIN, Macros.LOW_CARBS],
        ingredients=[
            Ingredient(name="chicken breast", quantity=300, unit="g", category="protein"),
            Ingredient(name="mixed greens", quantity=100, unit="g", category="vegetable"),
            Ingredient(name="cherry tomatoes", quantity=150, unit="g", category="vegetable"),
            Ingredient(name="cucumber", quantity=1, unit="piece", category="vegetable"),
            Ingredient(name="olive oil", quantity=3, unit="tbsp", category="oil"),
            Ingredient(name="lemon juice", quantity=2, unit="tbsp", category="liquid"),
            Ingredient(name="salt", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="black pepper", quantity=0.5, unit="tsp", category="spice"),
        ],
        equipment=[
            Equipment(name="grill", category="cookware"),
            Equipment(name="bowl", category="utensil"),
            Equipment(name="knife", category="utensil"),
        ],
        nutritional_info=NutritionalInfo(
            calories=320,
            protein=38,
            carbohydrates=12,
            fat=14,
            fiber=4,
            sodium=380
        ),
        instructions=[
            "Season chicken breast with salt and pepper",
            "Grill chicken for 6-7 minutes per side until cooked through",
            "Let chicken rest for 5 minutes, then slice",
            "Chop vegetables and mix in a bowl",
            "Add grilled chicken on top",
            "Drizzle with olive oil and lemon juice",
            "Toss and serve immediately"
        ],
        servings=2,
        prep_time=15,
        cuisine="Mediterranean",
        description="Healthy grilled chicken salad with fresh vegetables",
        cost=6.5
    ),
```

## Recipe Ideas to Get Started

Here are 20 recipe ideas you can implement:

1. **Breakfast Ideas:**
   - Overnight Oats (vegan, easy)
   - Greek Yogurt Parfait (vegetarian, easy)
   - Avocado Toast (vegetarian/vegan, easy)
   - Scrambled Eggs (vegetarian, easy)
   - Pancakes (vegetarian, medium)

2. **Lunch/Dinner Ideas:**
   - Grilled Salmon (pescatarian, medium)
   - Chicken Stir Fry (omnivore, easy)
   - Tofu Curry (vegan, medium)
   - Beef Tacos (omnivore, easy)
   - Vegetable Soup (vegan, easy)
   - Spaghetti Bolognese (omnivore, medium)
   - Caesar Salad (vegetarian, easy)
   - Quinoa Buddha Bowl (vegan, easy)
   - Fish Tacos (pescatarian, easy)

3. **Snacks/Desserts:**
   - Hummus with Vegetables (vegan, easy)
   - Protein Smoothie (vegetarian, easy)
   - Fruit Salad (vegan, easy)
   - Chocolate Chip Cookies (vegetarian, medium)
   - Banana Bread (vegetarian, medium)
   - Apple Slices with Peanut Butter (vegetarian, easy)

## Tips for Variety

To ensure good filtering, include recipes with:
- ✅ Different diets (vegan, vegetarian, pescatarian, omnivore)
- ✅ Different skill levels (easy, medium, experienced)
- ✅ Different cooking times (quick, medium, long)
- ✅ Different meal types (breakfast, lunch, dinner, snacks)
- ✅ Recipes with common allergens (eggs, dairy, nuts)
- ✅ Recipes without allergens (safe options)

## How to Add to the File

1. Open `data/sample_recipes.py`
2. Scroll to the end of the SAMPLE_RECIPES list (around line 250)
3. Find the last recipe (Dark Chocolate Energy Bites)
4. Add a comma after the closing `)` of that recipe
5. Paste your new recipe(s)
6. Make sure the final `]` is AFTER all your new recipes
7. Save the file

## Example of Adding Multiple Recipes

```python
# ... existing recipes ...

    Recipe(
        name="Dark Chocolate Energy Bites",
        # ... existing recipe content ...
        cost=4.5
    ),  # <-- ADD COMMA HERE
    
    Recipe(
        name="Your First New Recipe",
        # ... your recipe content ...
        cost=5.0
    ),
    
    Recipe(
        name="Your Second New Recipe",
        # ... your recipe content ...
        cost=3.5
    ),
    
    # Add 18 more recipes here...
    
]  # <-- Keep this closing bracket at the very end
```

## Testing Your Recipes

After adding recipes, run the tests to make sure everything works:

```bash
python -m pytest test_gui_inference.py -v
```

The tests will verify that:
- Allergen filtering works correctly
- Dietary restrictions are respected
- Skill levels are appropriate
- Time constraints are honored

## Questions?

If you have questions about:
- What values to use for Diet, Skill, etc. → Check the template above
- How to handle allergens → See the allergen table
- Recipe ideas → See the recipe ideas list

Good luck! 🍳
