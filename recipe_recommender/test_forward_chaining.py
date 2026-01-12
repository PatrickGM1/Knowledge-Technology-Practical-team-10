"""
Tests for forward-chaining inference engine and domain model
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
from pathlib import Path


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


def test_budget_constraint():
    """Test BudgetConstraint domain object"""
    print("\n=== Testing BudgetConstraint Domain Object ===")
    
    budget = BudgetConstraint(preferred_range="budget", flexibility="strict")
    
    # Create cheap recipe (should afford)
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
    
    # Create expensive recipe (should not afford with strict budget)
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
        cost=20.0  # Above budget range of 0-15
    )
    
    assert budget.can_afford(cheap_recipe), "Should afford budget recipe"
    print("✓ Budget constraint allows cheap recipe")
    
    assert not budget.can_afford(expensive_recipe), "Should not afford premium recipe with strict budget"
    print("✓ Budget constraint rejects expensive recipe")
    
    # Test flexible budget
    flexible_budget = BudgetConstraint(preferred_range="budget", flexibility="flexible")
    # Budget range 0-15, with 20% flexibility = 18 max, so use 17
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
        cost=17.0  # Within flexible budget (0-15 + 20% = 18)
    )
    assert flexible_budget.can_afford(moderately_expensive), "Flexible budget should allow moderately expensive recipe"
    print("✓ Flexible budget allows moderately expensive recipe")


def test_cooking_skill():
    """Test CookingSkill domain object"""
    print("\n=== Testing CookingSkill Domain Object ===")
    
    beginner = CookingSkill(level="beginner", years_experience=0)
    
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
    print("✓ Beginner can handle easy recipe")
    
    assert not beginner.can_handle(expert_recipe), "Beginner should not handle expert recipe"
    print("✓ Beginner cannot handle expert recipe")


def test_time_constraint():
    """Test TimeConstraint domain object"""
    print("\n=== Testing TimeConstraint Domain Object ===")
    
    # 30 minutes available
    time_limit = TimeConstraint(available_minutes=30, includes_prep=True, flexibility=False)
    
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
    
    assert time_limit.can_fit(quick_recipe), "Quick recipe should fit time constraint"
    print("✓ Time constraint allows quick recipe")
    
    assert not time_limit.can_fit(long_recipe), "Long recipe should not fit time constraint"
    print("✓ Time constraint rejects long recipe")


def test_kitchen_equipment():
    """Test Kitchen domain object"""
    print("\n=== Testing Kitchen Domain Object ===")
    
    kitchen = Kitchen(
        available_equipment=["pan", "pot", "oven"],
        available_utensils=["knife", "spoon"],
        space_size="medium"
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
    
    # Recipe requiring grill (not available)
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
    
    assert kitchen.can_prepare(pan_recipe), "Kitchen should have pan"
    print("✓ Kitchen has required equipment (pan)")
    
    assert not kitchen.can_prepare(grill_recipe), "Kitchen should not have grill"
    print("✓ Kitchen missing equipment (grill)")


def test_user_with_domain_objects():
    """Test User creation with domain objects"""
    print("\n=== Testing User with Domain Objects ===")
    
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
    assert recipe.suitable_for_user == True  # Default state
    assert recipe.recommendation_score == 0.0
    assert recipe.exclusion_reasons == []
    print("✓ Recipe states initialized correctly")


def test_forward_chaining_execution():
    """Test complete forward-chaining execution"""
    print("\n=== Testing Forward-Chaining Execution ===")
    
    # Create user
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
    
    # Create recipes
    recipes = [
        # Good match: vegetarian, budget, easy, quick
        Recipe(
            name="Simple Veggie Pasta",
            diet=Diet.VEGETARIAN,
            diet_restrictions=[DietRestriction.NONE],
            cooking_time=CookingTime.LESS_THAN_15,
            skill=Skill.EASY,
            cooking_methods=[CookingMethod.PAN],
            budget=Budget.BUDGET,
            meal=Meal.LUNCH,
            macros=[Macros.HIGH_PROTEIN],
            cost=3.0,
            equipment=[Equipment(name="pan", category="cookware")],
            prep_time=10
        ),
        # Bad match: expensive
        Recipe(
            name="Expensive Vegan Dish",
            diet=Diet.VEGAN,
            diet_restrictions=[DietRestriction.NONE],
            cooking_time=CookingTime.LESS_THAN_15,
            skill=Skill.EASY,
            cooking_methods=[CookingMethod.PAN],
            budget=Budget.PREMIUM,
            meal=Meal.DINNER,
            macros=[],
            cost=15.0,
            equipment=[Equipment(name="pan", category="cookware")],
            prep_time=10
        ),
        # Bad match: requires expert skill
        Recipe(
            name="Expert Recipe",
            diet=Diet.VEGETARIAN,
            diet_restrictions=[DietRestriction.NONE],
            cooking_time=CookingTime.LESS_THAN_15,
            skill=Skill.EXPERIENCED,
            cooking_methods=[CookingMethod.PAN],
            budget=Budget.BUDGET,
            meal=Meal.DINNER,
            macros=[],
            cost=3.0,
            equipment=[Equipment(name="pan", category="cookware")],
            prep_time=5
        )
    ]
    
    # Run forward-chaining
    kb_path = Path(__file__).parent / 'knowledge_base.yaml'
    engine = InferenceEngine(str(kb_path))
    
    engine.forward_chain(user, user.kitchen, recipes)
    
    # Get recommendations
    recommended = engine.get_recommended_recipes(recipes)
    
    print(f"\n  Total recipes: {len(recipes)}")
    print(f"  Recommended: {len(recommended)}")
    
    for recipe in recipes:
        print(f"\n  Recipe: {recipe.name}")
        print(f"    - suitable_for_user: {recipe.suitable_for_user}")
        print(f"    - affordable: {recipe.affordable}")
        print(f"    - can_prepare: {recipe.can_prepare}")
        print(f"    - skill_appropriate: {recipe.skill_appropriate}")
        print(f"    - recommendation_score: {recipe.recommendation_score}")
        if recipe.exclusion_reasons:
            print(f"    - exclusion_reasons: {recipe.exclusion_reasons}")
    
    # Assertions
    assert len(recommended) > 0, "Should have at least one recommendation"
    print(f"\n✓ Forward-chaining produced {len(recommended)} recommendations")
    
    # First recipe should be the good match
    if recommended:
        assert recommended[0].name == "Simple Veggie Pasta", "Best match should be Simple Veggie Pasta"
        assert recommended[0].recommendation_score > 0, "Best match should have positive score"
        print("✓ Best match identified correctly")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("TESTING FORWARD-CHAINING INFERENCE SYSTEM")
    print("=" * 60)
    
    try:
        test_allergy_domain_object()
        test_budget_constraint()
        test_cooking_skill()
        test_time_constraint()
        test_kitchen_equipment()
        test_user_with_domain_objects()
        test_forward_chaining_initialization()
        test_forward_chaining_execution()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
