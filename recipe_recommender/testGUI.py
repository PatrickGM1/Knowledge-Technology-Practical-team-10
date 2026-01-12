"""
Comprehensive GUI and system tests for Recipe Recommender
Tests all quiz questions, domain objects, inference engine, and user flows
"""
from models import (
    Recipe, Diet, DietRestriction, CookingTime, Skill, CookingMethod, 
    Budget, Meal, Macros, Ingredient, Equipment, NutritionalInfo
)
from models.allergy import Allergy
from models.budget_constraint import BudgetConstraint
from models.cooking_skill import CookingSkill
from models.time_constraint import TimeConstraint
from models.dietary_preference import DietaryPreference
from models.health_goal import HealthGoal
from models.kitchen import Kitchen
from models.user import User
from system.inference_engine import InferenceEngine
from system.utils import preferences_to_user
from data.sample_recipes import get_all_recipes
from pathlib import Path


# ============================================================================
# DOMAIN OBJECT TESTS
# ============================================================================

def test_allergy_domain_object():
    """Test Allergy domain object behavior"""
    print("\n=== Testing Allergy Domain Object ===")
    
    # Create allergy
    dairy_allergy = Allergy(allergen_name="dairy", severity="severe")
    
    # Test ingredient with dairy
    cheese = Ingredient(name="cheese", quantity=100, unit="g", category="dairy", allergens=["dairy"])
    
    assert not dairy_allergy.is_safe(cheese), "Cheese should not be safe for dairy allergy"
    print("✓ Dairy allergy correctly identifies unsafe ingredient")
    
    # Test safe ingredient
    tomato = Ingredient(name="tomato", quantity=2, unit="pieces", category="vegetable")
    assert dairy_allergy.is_safe(tomato), "Tomato should be safe for dairy allergy"
    print("✓ Dairy allergy correctly identifies safe ingredient")
    
    # Check auto-populated ingredients to avoid
    assert "milk" in dairy_allergy.ingredients_to_avoid
    assert "cheese" in dairy_allergy.ingredients_to_avoid
    print("✓ Allergy auto-populates ingredients to avoid")
    
    # Test nuts allergy
    nuts_allergy = Allergy(allergen_name="nuts", severity="moderate")
    almond = Ingredient(name="almonds", quantity=50, unit="g", category="protein", allergens=["nuts"])
    assert not nuts_allergy.is_safe(almond), "Almonds should not be safe for nuts allergy"
    print("✓ Nuts allergy correctly identifies unsafe ingredient")


def test_budget_constraint():
    """Test BudgetConstraint domain object"""
    print("\n=== Testing BudgetConstraint Domain Object ===")
    
    # Budget range
    budget = BudgetConstraint(preferred_range="budget", flexibility="strict")
    
    # Create cheap recipe
    cheap_recipe = Recipe(
        name="Simple Pasta",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET,
        meal=Meal.LUNCH,
        macros=[],
        cost=3.0
    )
    
    # Create expensive recipe
    expensive_recipe = Recipe(
        name="Luxury Meal",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.OVEN],
        budget=Budget.PREMIUM,
        meal=Meal.DINNER,
        macros=[],
        cost=30.0  # Premium range starts at 25
    )
    
    assert budget.can_afford(cheap_recipe), "Should afford budget recipe"
    print("✓ Budget constraint allows cheap recipe")
    
    assert not budget.can_afford(expensive_recipe), "Should not afford premium recipe with strict budget"
    print("✓ Budget constraint rejects expensive recipe")
    
    # Test flexible budget
    flexible_budget = BudgetConstraint(preferred_range="budget", flexibility="flexible")
    moderately_expensive = Recipe(
        name="Mid-Range Meal",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.OVEN],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[],
        cost=17.0
    )
    assert flexible_budget.can_afford(moderately_expensive), "Flexible budget should allow moderately expensive recipe"
    print("✓ Flexible budget allows moderately expensive recipe")
    
    # Test moderate budget
    moderate_budget = BudgetConstraint(preferred_range="moderate", flexibility="strict")
    assert moderate_budget.can_afford(moderately_expensive), "Moderate budget should afford moderate recipe"
    print("✓ Moderate budget constraint works correctly")
    
    # Test premium budget
    premium_budget = BudgetConstraint(preferred_range="premium", flexibility="strict")
    assert premium_budget.can_afford(expensive_recipe), "Premium budget should afford expensive recipe"
    print("✓ Premium budget constraint allows expensive recipes")


def test_cooking_skill():
    """Test CookingSkill domain object"""
    print("\n=== Testing CookingSkill Domain Object ===")
    
    beginner = CookingSkill(level="beginner", years_experience=0)
    intermediate = CookingSkill(level="intermediate", years_experience=3)
    advanced = CookingSkill(level="advanced", years_experience=10)
    
    # Easy recipe
    easy_recipe = Recipe(
        name="Toast",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET,
        meal=Meal.BREAKFAST,
        macros=[]
    )
    
    # Medium recipe
    medium_recipe = Recipe(
        name="Risotto",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[]
    )
    
    # Expert recipe
    expert_recipe = Recipe(
        name="Beef Wellington",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.MORE_THAN_45,
        skill=Skill.EXPERIENCED,
        cooking_methods=[CookingMethod.OVEN],
        budget=Budget.PREMIUM,
        meal=Meal.DINNER,
        macros=[]
    )
    
    assert beginner.can_handle(easy_recipe), "Beginner should handle easy recipe"
    assert not beginner.can_handle(expert_recipe), "Beginner should not handle expert recipe"
    print("✓ Beginner skill level works correctly")
    
    assert intermediate.can_handle(easy_recipe), "Intermediate should handle easy recipe"
    assert intermediate.can_handle(medium_recipe), "Intermediate should handle medium recipe"
    assert not intermediate.can_handle(expert_recipe), "Intermediate should not handle expert recipe"
    print("✓ Intermediate skill level works correctly")
    
    assert advanced.can_handle(easy_recipe), "Advanced should handle easy recipe"
    assert advanced.can_handle(medium_recipe), "Advanced should handle medium recipe"
    assert advanced.can_handle(expert_recipe), "Advanced should handle expert recipe"
    print("✓ Advanced skill level works correctly")


def test_time_constraint():
    """Test TimeConstraint domain object"""
    print("\n=== Testing TimeConstraint Domain Object ===")
    
    # Less than 15 minutes - but need to account for prep + cook time
    quick_time = TimeConstraint(available_minutes=20, includes_prep=True, flexibility=False)
    
    # 30 minutes available - but 15-45 maps to 30 cook + prep, so need more
    medium_time = TimeConstraint(available_minutes=60, includes_prep=True, flexibility=False)
    
    # Over 45 minutes - > 45 maps to 60 cook + 20 prep = 80 total
    long_time = TimeConstraint(available_minutes=90, includes_prep=True, flexibility=False)
    
    # Quick recipe
    quick_recipe = Recipe(
        name="Quick Salad",
        diet=Diet.VEGAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET,
        meal=Meal.LUNCH,
        macros=[],
        prep_time=10
    )
    
    # Medium recipe
    medium_recipe = Recipe(
        name="Pasta",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET,
        meal=Meal.LUNCH,
        macros=[],
        prep_time=20
    )
    
    # Long recipe
    long_recipe = Recipe(
        name="Slow Roast",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.MORE_THAN_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.OVEN],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[],
        prep_time=20
    )
    
    assert quick_time.can_fit(quick_recipe), "Quick time should fit quick recipe"
    assert not quick_time.can_fit(long_recipe), "Quick time should not fit long recipe"
    print("✓ < 15 min time constraint works correctly")
    
    assert medium_time.can_fit(quick_recipe), "Medium time should fit quick recipe"
    assert medium_time.can_fit(medium_recipe), "Medium time should fit medium recipe"
    assert not medium_time.can_fit(long_recipe), "Medium time should not fit long recipe"
    print("✓ 15-45 min time constraint works correctly")
    
    assert long_time.can_fit(quick_recipe), "Long time should fit quick recipe"
    assert long_time.can_fit(medium_recipe), "Long time should fit medium recipe"
    assert long_time.can_fit(long_recipe), "Long time should fit long recipe"
    print("✓ > 45 min time constraint works correctly")


def test_dietary_preferences():
    """Test DietaryPreference domain object"""
    print("\n=== Testing DietaryPreference Domain Object ===")
    
    # Vegan preference
    vegan = DietaryPreference(type="vegan", restrictions=[], preferred_cuisines=[])
    
    # Vegetarian preference
    vegetarian = DietaryPreference(type="vegetarian", restrictions=[], preferred_cuisines=[])
    
    # Omnivore preference
    omnivore = DietaryPreference(type="omnivore", restrictions=[], preferred_cuisines=[])
    
    # Vegan recipe
    vegan_recipe = Recipe(
        name="Vegan Salad",
        diet=Diet.VEGAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET,
        meal=Meal.LUNCH,
        macros=[]
    )
    
    # Vegetarian recipe
    veg_recipe = Recipe(
        name="Cheese Pizza",
        diet=Diet.VEGETARIAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.OVEN],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[]
    )
    
    # Meat recipe
    meat_recipe = Recipe(
        name="Steak",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.GRILL],
        budget=Budget.PREMIUM,
        meal=Meal.DINNER,
        macros=[]
    )
    
    assert vegan.is_compatible(vegan_recipe), "Vegan should accept vegan recipe"
    assert not vegan.is_compatible(veg_recipe), "Vegan should not accept vegetarian recipe with dairy"
    assert not vegan.is_compatible(meat_recipe), "Vegan should not accept meat recipe"
    print("✓ Vegan dietary preference works correctly")
    
    assert vegetarian.is_compatible(vegan_recipe), "Vegetarian should accept vegan recipe"
    assert vegetarian.is_compatible(veg_recipe), "Vegetarian should accept vegetarian recipe"
    assert not vegetarian.is_compatible(meat_recipe), "Vegetarian should not accept meat recipe"
    print("✓ Vegetarian dietary preference works correctly")
    
    assert omnivore.is_compatible(vegan_recipe), "Omnivore should accept vegan recipe"
    assert omnivore.is_compatible(veg_recipe), "Omnivore should accept vegetarian recipe"
    assert omnivore.is_compatible(meat_recipe), "Omnivore should accept meat recipe"
    print("✓ Omnivore dietary preference works correctly")


def test_health_goals():
    """Test HealthGoal domain object"""
    print("\n=== Testing HealthGoal Domain Object ===")
    
    high_protein = HealthGoal(goal_type="high-protein", priority="high")
    low_fat = HealthGoal(goal_type="low-fat", priority="medium")
    low_carb = HealthGoal(goal_type="low-carb", priority="high")
    
    # High protein recipe
    protein_recipe_nutrition = NutritionalInfo(
        calories=400,
        protein=35,  # High protein
        carbohydrates=30,
        fat=10,
        fiber=5
    )
    
    # Low fat recipe
    lowfat_recipe_nutrition = NutritionalInfo(
        calories=300,
        protein=15,
        carbohydrates=50,
        fat=5,  # Low fat
        fiber=8
    )
    
    # Low carb recipe
    lowcarb_recipe_nutrition = NutritionalInfo(
        calories=350,
        protein=30,
        carbohydrates=10,  # Low carbs
        fat=20,
        fiber=3
    )
    
    assert high_protein.matches(protein_recipe_nutrition), "High protein goal should match high protein nutrition"
    print("✓ High protein health goal works correctly")
    
    assert low_fat.matches(lowfat_recipe_nutrition), "Low fat goal should match low fat nutrition"
    print("✓ Low fat health goal works correctly")
    
    assert low_carb.matches(lowcarb_recipe_nutrition), "Low carb goal should match low carb nutrition"
    print("✓ Low carb health goal works correctly")


def test_kitchen_equipment():
    """Test Kitchen domain object"""
    print("\n=== Testing Kitchen Domain Object ===")
    
    # Basic kitchen
    basic_kitchen = Kitchen(
        available_equipment=["pan", "pot"],
        available_utensils=["knife", "spoon"],
        space_size="small"
    )
    
    # Advanced kitchen
    advanced_kitchen = Kitchen(
        available_equipment=["pan", "pot", "oven", "grill"],
        available_utensils=["knife", "spoon", "whisk", "tongs"],
        space_size="large"
    )
    
    # Recipe requiring pan
    pan_recipe = Recipe(
        name="Stir Fry",
        diet=Diet.VEGAN,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.LESS_THAN_15,
        skill=Skill.EASY,
        cooking_methods=[CookingMethod.PAN],
        budget=Budget.BUDGET,
        meal=Meal.DINNER,
        macros=[],
        equipment=[Equipment(name="pan", category="cookware")]
    )
    
    # Recipe requiring oven
    oven_recipe = Recipe(
        name="Baked Chicken",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.OVEN],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[],
        equipment=[Equipment(name="oven", category="appliance")]
    )
    
    # Recipe requiring grill
    grill_recipe = Recipe(
        name="BBQ",
        diet=Diet.OMNIVORE,
        diet_restrictions=[DietRestriction.NONE],
        cooking_time=CookingTime.BETWEEN_15_45,
        skill=Skill.MEDIUM,
        cooking_methods=[CookingMethod.GRILL],
        budget=Budget.MODERATE,
        meal=Meal.DINNER,
        macros=[],
        equipment=[Equipment(name="grill", category="cookware")]
    )
    
    assert basic_kitchen.can_prepare(pan_recipe), "Basic kitchen should have pan"
    assert not basic_kitchen.can_prepare(oven_recipe), "Basic kitchen should not have oven"
    assert not basic_kitchen.can_prepare(grill_recipe), "Basic kitchen should not have grill"
    print("✓ Basic kitchen equipment checking works correctly")
    
    assert advanced_kitchen.can_prepare(pan_recipe), "Advanced kitchen should have pan"
    assert advanced_kitchen.can_prepare(oven_recipe), "Advanced kitchen should have oven"
    assert advanced_kitchen.can_prepare(grill_recipe), "Advanced kitchen should have grill"
    print("✓ Advanced kitchen equipment checking works correctly")


# ============================================================================
# QUIZ PREFERENCE TESTS
# ============================================================================

def test_diet_preferences():
    """Test all diet preference options from quiz"""
    print("\n=== Testing Diet Preferences from Quiz ===")
    
    # Test vegan preferences
    vegan_prefs = {'diet': [Diet.VEGAN], 'diet_restrictions': [DietRestriction.NONE]}
    user = preferences_to_user(vegan_prefs)
    assert user.dietary_preference.type == "vegan", "Should create vegan user"
    print("✓ Vegan diet preference")
    
    # Test vegetarian preferences
    veg_prefs = {'diet': [Diet.VEGETARIAN], 'diet_restrictions': [DietRestriction.NONE]}
    user = preferences_to_user(veg_prefs)
    assert user.dietary_preference.type == "vegetarian", "Should create vegetarian user"
    print("✓ Vegetarian diet preference")
    
    # Test pescatarian preferences
    pesc_prefs = {'diet': [Diet.PESCATARIAN], 'diet_restrictions': [DietRestriction.NONE]}
    user = preferences_to_user(pesc_prefs)
    assert user.dietary_preference.type == "pescatarian", "Should create pescatarian user"
    print("✓ Pescatarian diet preference")
    
    # Test omnivore preferences
    omni_prefs = {'diet': [Diet.OMNIVORE], 'diet_restrictions': [DietRestriction.NONE]}
    user = preferences_to_user(omni_prefs)
    assert user.dietary_preference.type == "omnivore", "Should create omnivore user"
    print("✓ Omnivore diet preference")


def test_dietary_restrictions():
    """Test all dietary restriction options from quiz"""
    print("\n=== Testing Dietary Restrictions from Quiz ===")
    
    # Test lactose intolerant
    lactose_prefs = {'diet': [Diet.OMNIVORE], 'diet_restrictions': [DietRestriction.LACTOSE_INTOLERANT]}
    user = preferences_to_user(lactose_prefs)
    assert len(user.allergies_list) > 0, "Should have dairy allergy"
    print("✓ Lactose intolerant restriction")
    
    # Test gluten intolerant
    gluten_prefs = {'diet': [Diet.OMNIVORE], 'diet_restrictions': [DietRestriction.GLUTEN_INTOLERANT]}
    user = preferences_to_user(gluten_prefs)
    assert len(user.allergies_list) > 0, "Should have gluten allergy"
    print("✓ Gluten intolerant restriction")
    
    # Test nuts allergies
    nuts_prefs = {'diet': [Diet.OMNIVORE], 'diet_restrictions': [DietRestriction.NUTS_ALLERGIES]}
    user = preferences_to_user(nuts_prefs)
    assert len(user.allergies_list) > 0, "Should have nuts allergy"
    print("✓ Nuts allergies restriction")
    
    # Test diabetes
    diabetes_prefs = {'diet': [Diet.OMNIVORE], 'diet_restrictions': [DietRestriction.DIABETES]}
    user = preferences_to_user(diabetes_prefs)
    assert 'low-sugar' in user.dietary_restrictions, "Should have diabetes restriction"
    print("✓ Diabetes restriction")


def test_cooking_time_options():
    """Test all cooking time options from quiz"""
    print("\n=== Testing Cooking Time Options from Quiz ===")
    
    # Test < 15 min
    quick_prefs = {'cooking_time': [CookingTime.LESS_THAN_15]}
    user = preferences_to_user(quick_prefs)
    assert user.time_constraint is not None, "Should have time constraint"
    assert user.time_constraint.available_minutes <= 15, "Should be quick time"
    print("✓ < 15 min option")
    
    # Test 15-45 min
    medium_prefs = {'cooking_time': [CookingTime.BETWEEN_15_45]}
    user = preferences_to_user(medium_prefs)
    assert user.time_constraint is not None, "Should have time constraint"
    print("✓ 15-45 min option")
    
    # Test > 45 min
    long_prefs = {'cooking_time': [CookingTime.MORE_THAN_45]}
    user = preferences_to_user(long_prefs)
    assert user.time_constraint is None or user.time_constraint.available_minutes > 45, "Should be long time"
    print("✓ > 45 min option")


def test_skill_level_options():
    """Test all skill level options from quiz"""
    print("\n=== Testing Skill Level Options from Quiz ===")
    
    # Test beginner/easy
    beginner_prefs = {'skill': [Skill.EASY]}
    user = preferences_to_user(beginner_prefs)
    assert user.skill.level == "beginner", "Should be beginner skill"
    print("✓ Easy/Beginner skill level")
    
    # Test medium/intermediate
    medium_prefs = {'skill': [Skill.MEDIUM]}
    user = preferences_to_user(medium_prefs)
    assert user.skill.level in ["intermediate", "medium"], "Should be intermediate skill"
    print("✓ Medium/Intermediate skill level")
    
    # Test experienced/advanced
    expert_prefs = {'skill': [Skill.EXPERIENCED]}
    user = preferences_to_user(expert_prefs)
    assert user.skill.level in ["advanced", "experienced"], "Should be advanced skill"
    print("✓ Experienced/Advanced skill level")


def test_cooking_method_options():
    """Test all cooking method options from quiz"""
    print("\n=== Testing Cooking Method Options from Quiz ===")
    
    # Test pan
    pan_prefs = {'cooking_methods': [CookingMethod.PAN]}
    user = preferences_to_user(pan_prefs)
    assert 'pan' in user.kitchen.available_equipment, "Should have pan"
    print("✓ Pan cooking method")
    
    # Test oven
    oven_prefs = {'cooking_methods': [CookingMethod.OVEN]}
    user = preferences_to_user(oven_prefs)
    assert 'oven' in user.kitchen.available_equipment, "Should have oven"
    print("✓ Oven cooking method")
    
    # Test grill
    grill_prefs = {'cooking_methods': [CookingMethod.GRILL]}
    user = preferences_to_user(grill_prefs)
    assert 'grill' in user.kitchen.available_equipment, "Should have grill"
    print("✓ Grill cooking method")


def test_budget_options():
    """Test all budget options from quiz"""
    print("\n=== Testing Budget Options from Quiz ===")
    
    # Test budget
    budget_prefs = {'budget': [Budget.BUDGET]}
    user = preferences_to_user(budget_prefs)
    assert user.budget.preferred_range == "budget", "Should be budget range"
    print("✓ Budget option")
    
    # Test moderate
    moderate_prefs = {'budget': [Budget.MODERATE]}
    user = preferences_to_user(moderate_prefs)
    assert user.budget.preferred_range == "moderate", "Should be moderate range"
    print("✓ Moderate option")
    
    # Test premium
    premium_prefs = {'budget': [Budget.PREMIUM]}
    user = preferences_to_user(premium_prefs)
    assert user.budget.preferred_range == "premium", "Should be premium range"
    print("✓ Premium option")


def test_meal_type_options():
    """Test all meal type options from quiz"""
    print("\n=== Testing Meal Type Options from Quiz ===")
    
    meal_types = [
        (Meal.BREAKFAST, "breakfast"),
        (Meal.LUNCH, "lunch"),
        (Meal.DINNER, "dinner"),
        (Meal.SNACK, "snack"),
        (Meal.DESSERT, "dessert")
    ]
    
    for meal_enum, meal_name in meal_types:
        prefs = {'meal': [meal_enum]}
        user = preferences_to_user(prefs)
        # Just verify it doesn't crash
        print(f"✓ {meal_name.title()} meal type")


def test_macro_options():
    """Test all macro/nutritional goal options from quiz"""
    print("\n=== Testing Macro/Nutritional Goal Options from Quiz ===")
    
    # Test high protein
    protein_prefs = {'macros': [Macros.HIGH_PROTEIN]}
    user = preferences_to_user(protein_prefs)
    assert len(user.health_goals_list) > 0, "Should have health goals"
    assert any(g.goal_type == "high-protein" for g in user.health_goals_list), "Should have high protein goal"
    print("✓ High protein macro")
    
    # Test low fats
    lowfat_prefs = {'macros': [Macros.LOW_FATS]}
    user = preferences_to_user(lowfat_prefs)
    assert any(g.goal_type == "low-fat" for g in user.health_goals_list), "Should have low fat goal"
    print("✓ Low fats macro")
    
    # Test low carbs
    lowcarb_prefs = {'macros': [Macros.LOW_CARBS]}
    user = preferences_to_user(lowcarb_prefs)
    assert any(g.goal_type == "low-carb" for g in user.health_goals_list), "Should have low carb goal"
    print("✓ Low carbs macro")
    
    # Test low sugars
    lowsugar_prefs = {'macros': [Macros.LOW_SUGARS]}
    user = preferences_to_user(lowsugar_prefs)
    assert any(g.goal_type == "low-sugar" for g in user.health_goals_list), "Should have low sugar goal"
    print("✓ Low sugars macro")


# ============================================================================
# INFERENCE ENGINE TESTS
# ============================================================================

def test_forward_chaining_initialization():
    """Test forward-chaining recipe state initialization"""
    print("\n=== Testing Forward-Chaining Initialization ===")
    
    kb_path = Path(__file__).parent / 'knowledge_base.yaml'
    engine = InferenceEngine(str(kb_path))
    
    recipes = [
        Recipe(
            name="Test Recipe",
            diet=Diet.VEGETARIAN,
            diet_restrictions=[DietRestriction.NONE],
            cooking_time=CookingTime.LESS_THAN_15,
            skill=Skill.EASY,
            cooking_methods=[CookingMethod.PAN],
            budget=Budget.BUDGET,
            meal=Meal.LUNCH,
            macros=[],
            cost=3.0
        )
    ]
    
    engine.initialize_recipe_states(recipes)
    
    recipe = recipes[0]
    assert hasattr(recipe, 'suitable_for_user')
    assert recipe.suitable_for_user == True
    assert recipe.recommendation_score == 0.0
    assert recipe.exclusion_reasons == []
    print("✓ Recipe states initialized correctly")


def test_forward_chaining_with_sample_recipes():
    """Test forward-chaining with actual sample recipes"""
    print("\n=== Testing Forward-Chaining with Sample Recipes ===")
    
    # Create a budget-conscious vegetarian user
    user = User(
        name="Budget Vegetarian",
        dietary_restrictions=[],
        allergies=[],
        skill_level="beginner",
        available_equipment=["pan", "pot"],
        max_cooking_time=30,
        health_goals=["high-protein"],
        allergies_list=[],
        budget=BudgetConstraint(preferred_range="budget", flexibility="strict"),
        skill=CookingSkill(level="beginner", years_experience=1),
        time_constraint=TimeConstraint(available_minutes=30, includes_prep=True, flexibility=False),
        dietary_preference=DietaryPreference(type="vegetarian", restrictions=[], preferred_cuisines=[]),
        health_goals_list=[HealthGoal(goal_type="high-protein", priority="high")],
        kitchen=Kitchen(available_equipment=["pan", "pot"], available_utensils=[], space_size="small")
    )
    
    # Get sample recipes
    all_recipes = get_all_recipes()
    
    # Run forward-chaining
    kb_path = Path(__file__).parent / 'knowledge_base.yaml'
    engine = InferenceEngine(str(kb_path))
    
    engine.forward_chain(user, user.kitchen, all_recipes)
    
    # Get recommendations
    recommended = engine.get_recommended_recipes(all_recipes)
    
    print(f"  Total recipes: {len(all_recipes)}")
    print(f"  Recommended: {len(recommended)}")
    
    if recommended:
        print(f"  Top recommendation: {recommended[0].name}")
        print(f"  Score: {recommended[0].recommendation_score}")
    
    assert isinstance(recommended, list), "Should return a list"
    print("✓ Forward-chaining works with sample recipes")


def test_user_with_all_domain_objects():
    """Test User creation with all domain objects populated"""
    print("\n=== Testing User with All Domain Objects ===")
    
    user = User(
        name="Test User",
        dietary_restrictions=["dairy"],
        allergies=["dairy"],
        skill_level="beginner",
        available_equipment=["pan", "pot"],
        max_cooking_time=30,
        health_goals=["high-protein"],
        # Domain objects
        allergies_list=[Allergy(allergen_name="dairy", severity="moderate")],
        budget=BudgetConstraint(preferred_range="budget", flexibility="flexible"),
        skill=CookingSkill(level="beginner", years_experience=0),
        time_constraint=TimeConstraint(available_minutes=30, includes_prep=True, flexibility=False),
        dietary_preference=DietaryPreference(type="vegetarian", restrictions=["dairy"], preferred_cuisines=[]),
        health_goals_list=[HealthGoal(goal_type="high-protein", priority="high")],
        kitchen=Kitchen(available_equipment=["pan", "pot"], available_utensils=[], space_size="small")
    )
    
    assert len(user.allergies_list) == 1
    assert user.allergies_list[0].allergen_name == "dairy"
    print("✓ User has allergy domain objects")
    
    assert user.budget.preferred_range == "budget"
    print("✓ User has budget constraint")
    
    assert user.skill.level == "beginner"
    print("✓ User has skill level")
    
    assert user.kitchen.available_equipment == ["pan", "pot"]
    print("✓ User has kitchen object")
    
    assert user.time_constraint.available_minutes == 30
    print("✓ User has time constraint")
    
    assert user.dietary_preference.type == "vegetarian"
    print("✓ User has dietary preference")
    
    assert len(user.health_goals_list) == 1
    print("✓ User has health goals")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_complete_user_flow():
    """Test complete user flow from quiz to recommendations"""
    print("\n=== Testing Complete User Flow ===")
    
    # Simulate quiz answers
    preferences = {
        'diet': [Diet.VEGETARIAN],
        'diet_restrictions': [DietRestriction.LACTOSE_INTOLERANT],
        'cooking_time': [CookingTime.LESS_THAN_15],
        'skill': [Skill.EASY],
        'cooking_methods': [CookingMethod.PAN],
        'budget': [Budget.BUDGET],
        'meal': [Meal.LUNCH],
        'macros': [Macros.HIGH_PROTEIN, Macros.LOW_FATS]
    }
    
    # Convert to user
    user = preferences_to_user(preferences)
    
    # Verify user was created correctly
    assert user.dietary_preference.type == "vegetarian"
    assert len(user.allergies_list) > 0
    assert user.budget.preferred_range == "budget"
    assert user.skill.level == "beginner"
    print("✓ User created from quiz preferences")
    
    # Get recipes
    all_recipes = get_all_recipes()
    
    # Run inference
    kb_path = Path(__file__).parent / 'knowledge_base.yaml'
    engine = InferenceEngine(str(kb_path))
    engine.forward_chain(user, user.kitchen, all_recipes)
    
    # Get recommendations
    recommended = engine.get_recommended_recipes(all_recipes)
    
    print(f"  User preferences: Vegetarian, Lactose Intolerant, < 15 min, Easy, Budget")
    print(f"  Recipes found: {len(recommended)}")
    
    if recommended:
        for i, recipe in enumerate(recommended[:3], 1):
            print(f"  {i}. {recipe.name} (Score: {recipe.recommendation_score})")
    
    print("✓ Complete flow from quiz to recommendations works")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("COMPREHENSIVE GUI AND SYSTEM TESTS")
    print("Recipe Recommender System")
    print("=" * 60)
    
    try:
        # Domain object tests
        test_allergy_domain_object()
        test_budget_constraint()
        test_cooking_skill()
        test_time_constraint()
        test_dietary_preferences()
        test_health_goals()
        test_kitchen_equipment()
        
        # Quiz preference tests
        test_diet_preferences()
        test_dietary_restrictions()
        test_cooking_time_options()
        test_skill_level_options()
        test_cooking_method_options()
        test_budget_options()
        test_meal_type_options()
        test_macro_options()
        
        # Inference engine tests
        test_forward_chaining_initialization()
        test_forward_chaining_with_sample_recipes()
        test_user_with_all_domain_objects()
        
        # Integration tests
        test_complete_user_flow()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
