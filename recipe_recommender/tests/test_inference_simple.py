"""Test suite for forward-chaining inference engine"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from inference.inference_engine import InferenceEngine
from constraints.user import User
from domainClasses.recipe import Recipe
from domainClasses.ingredient import Ingredient
from domainClasses.equipment import Equipment
from domainClasses.nutritional_info import NutritionalInfo


def test_inference_derives_facts():
    """Verify inference engine derives facts"""
    
    # Load inference engine
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    # Create simple user with dairy allergy
    user = User(
        name="Test User",
        allergies=["dairy"],
        available_equipment=["oven", "pan"],
        skill_level="beginner"
    )
    
    # Create simple recipe with dairy
    recipe = Recipe(
        name="Cheese Pasta",
        ingredients=[
            Ingredient(name="pasta", quantity=200, unit="g"),
            Ingredient(name="cheese", quantity=100, unit="g", allergens=["dairy"])
        ],
        cuisine="Italian",
        nutritional_info=NutritionalInfo(calories=400, protein=20, carbohydrates=50, fat=12)
    )
    
    
    
    # RUN INFERENCE
    recommended_recipes = engine.forward_chain(user, user, [recipe])
    
    if engine.working_memory:
        for i, fact in enumerate(sorted(engine.working_memory), 1):
            pass
        pass
    else:
        pass
    
    
    # VERIFY INFERENCE HAPPENED
    assert len(engine.working_memory) > 0, "❌ No facts derived - might be filtering!"
    
    
    # Check for specific inference patterns
    allergy_facts = [f for f in engine.working_memory if 'allerg' in f.lower()]
    dairy_facts = [f for f in engine.working_memory if 'dairy' in f.lower()]
    
    
    if allergy_facts:
        for fact in allergy_facts[:3]:
            pass
    


    pass
    


def test_iterative_rule_firing():
    """
    TEST: Verify rules fire iteratively until fixed point
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Vegan User",
        dietary_restrictions=["vegan"],
        available_equipment=["blender", "oven"],
        skill_level="intermediate"
    )
    
    recipe1 = Recipe(
        name="Chicken Soup",
        ingredients=[
            Ingredient(name="chicken", quantity=300, unit="g"),
            Ingredient(name="vegetables", quantity=200, unit="g")
        ],
        cuisine="American"
    )
    
    recipe2 = Recipe(
        name="Lentil Soup",
        ingredients=[
            Ingredient(name="lentils", quantity=200, unit="g"),
            Ingredient(name="vegetables", quantity=200, unit="g")
        ],
        cuisine="Mediterranean",
        diet="vegan"
    )
    
    
    recommended_recipes = engine.forward_chain(user, user, [recipe1, recipe2])
    
    
    # Show chain of inference
    vegan_facts = [f for f in engine.working_memory if 'vegan' in f.lower()]
    for fact in vegan_facts[:5]:
        pass
    
    assert len(engine.working_memory) >= 2, "Not enough facts - rules didn't chain"
    


def test_allergy_detection_and_exclusion():
    """
    TEST: Verify allergy detection triggers exclusion rules
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Allergic User",
        allergies=["nuts", "dairy", "gluten"],
        available_equipment=["oven", "blender"],
        skill_level="intermediate",
        budget=25.0
    )
    
    # Recipe 1: Contains nuts
    recipe1 = Recipe(
        name="Almond Cake",
        ingredients=[
            Ingredient(name="almonds", quantity=200, unit="g", allergens=["nuts"]),
            Ingredient(name="flour", quantity=150, unit="g", allergens=["gluten"])
        ],
        cuisine="French"
    )
    
    # Recipe 2: Contains dairy
    recipe2 = Recipe(
        name="Cheese Pizza",
        ingredients=[
            Ingredient(name="cheese", quantity=200, unit="g", allergens=["dairy"]),
            Ingredient(name="dough", quantity=300, unit="g")
        ],
        cuisine="Italian"
    )
    
    # Recipe 3: Safe recipe
    recipe3 = Recipe(
        name="Fruit Salad",
        ingredients=[
            Ingredient(name="apple", quantity=2, unit="pieces"),
            Ingredient(name="banana", quantity=2, unit="pieces")
        ],
        cuisine="International"
    )
    
    
    recommended = engine.forward_chain(user, user, [recipe1, recipe2, recipe3])
    
    
    allergy_facts = [f for f in engine.working_memory if 'allergic' in f.lower()]
    for fact in allergy_facts:
        pass

    assert any('nuts' in f.lower() for f in engine.working_memory), "Nut allergy not detected"
    assert any('dairy' in f.lower() for f in engine.working_memory), "Dairy allergy not detected"
    assert any('gluten' in f.lower() for f in engine.working_memory), "Gluten allergy not detected"
    


def test_equipment_compatibility():
    """
    TEST: Verify equipment matching and incompatibility detection
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Limited Kitchen User",
        allergies=[],
        available_equipment=["microwave", "knife"],
        skill_level="beginner",
        budget=30.0
    )
    
    # Recipe needs oven
    recipe1 = Recipe(
        name="Roasted Chicken",
        ingredients=[Ingredient(name="chicken", quantity=1, unit="kg")],
        equipment=[Equipment(name="oven"), Equipment(name="roasting pan")],
        cuisine="American"
    )
    
    # Recipe needs only microwave
    recipe2 = Recipe(
        name="Microwave Oatmeal",
        ingredients=[Ingredient(name="oats", quantity=100, unit="g")],
        equipment=[Equipment(name="microwave"), Equipment(name="bowl")],
        cuisine="International"
    )
    
    
    recommended = engine.forward_chain(user, user, [recipe1, recipe2])
    
    equipment_facts = [f for f in engine.working_memory if 'equipment' in f.lower()]
    for fact in equipment_facts[:10]:
        pass
    
    assert len(equipment_facts) > 0, "No equipment facts derived"
    


def test_dietary_preferences():
    """
    TEST: Verify dietary preference handling (vegan, vegetarian, etc.)
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Vegan User",
        allergies=[],
        dietary_restrictions=["vegan"],
        available_equipment=["stove", "blender"],
        skill_level="advanced"
    )
    
    recipe1 = Recipe(
        name="Beef Stew",
        ingredients=[Ingredient(name="beef", quantity=500, unit="g")],
        cuisine="American",
        diet="omnivore"
    )
    
    recipe2 = Recipe(
        name="Tofu Stir Fry",
        ingredients=[
            Ingredient(name="tofu", quantity=300, unit="g"),
            Ingredient(name="vegetables", quantity=200, unit="g")
        ],
        cuisine="Asian",
        diet="vegan"
    )
    
    recipe3 = Recipe(
        name="Cheese Omelette",
        ingredients=[
            Ingredient(name="eggs", quantity=3, unit="pieces", allergens=["eggs"]),
            Ingredient(name="cheese", quantity=50, unit="g", allergens=["dairy"])
        ],
        cuisine="French",
        diet="vegetarian"
    )
    
    
    recommended = engine.forward_chain(user, user, [recipe1, recipe2, recipe3])
    
    diet_facts = [f for f in engine.working_memory if 'diet' in f.lower() or 'vegan' in f.lower()]
    for fact in diet_facts[:8]:
        pass
    
    assert any('vegan' in f.lower() for f in engine.working_memory), "Vegan preference not detected"
    


def test_skill_level_matching():
    """
    TEST: Verify skill level appropriateness checking
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Beginner Cook",
        allergies=[],
        available_equipment=["microwave", "pan"],
        skill_level="beginner",
        budget=20.0
    )
    
    recipe1 = Recipe(
        name="Simple Toast",
        ingredients=[Ingredient(name="bread", quantity=2, unit="slices")],
        cuisine="International",
        skill="easy"
    )
    
    recipe2 = Recipe(
        name="Beef Wellington",
        ingredients=[Ingredient(name="beef", quantity=800, unit="g")],
        cuisine="British",
        skill="experienced"
    )
    
    
    recommended = engine.forward_chain(user, user, [recipe1, recipe2])
    
    skill_facts = [f for f in engine.working_memory if 'skill' in f.lower()]
    for fact in skill_facts:
        pass
    
    assert len(skill_facts) > 0, "No skill facts derived"
    


def test_budget_constraints():
    """
    TEST: Verify budget constraint checking
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Budget User",
        allergies=[],
        available_equipment=["pan", "pot"],
        skill_level="intermediate",
        budget=10.0
    )
    
    recipe1 = Recipe(
        name="Cheap Pasta",
        ingredients=[Ingredient(name="pasta", quantity=200, unit="g")],
        cuisine="Italian",
        cost=5.0,
        budget="low"
    )
    
    recipe2 = Recipe(
        name="Expensive Lobster",
        ingredients=[Ingredient(name="lobster", quantity=500, unit="g")],
        cuisine="French",
        cost=50.0,
        budget="premium"
    )
    
    
    recommended = engine.forward_chain(user, user, [recipe1, recipe2])
    
    budget_facts = [f for f in engine.working_memory if 'budget' in f.lower()]
    for fact in budget_facts:
        pass
    
    assert len(budget_facts) > 0, "No budget facts derived"
    


def test_working_memory_accumulation():
    """
    TEST: Verify working memory accumulates facts across iterations
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Complex User",
        allergies=["nuts", "shellfish"],
        dietary_restrictions=["vegetarian"],
        available_equipment=["oven", "blender", "microwave"],
        skill_level="advanced",
        budget=50.0,
        health_goals=["low-calorie", "high-protein"]
    )
    
    recipe = Recipe(
        name="Veggie Bowl",
        ingredients=[
            Ingredient(name="quinoa", quantity=200, unit="g"),
            Ingredient(name="vegetables", quantity=300, unit="g")
        ],
        cuisine="Healthy",
        nutritional_info=NutritionalInfo(calories=350, protein=15, carbohydrates=60, fat=8)
    )
    
    
    initial_facts = len(engine.working_memory)
    recommended = engine.forward_chain(user, user, [recipe])
    
    final_facts = len(engine.working_memory)
    
    
    for i, fact in enumerate(sorted(engine.working_memory), 1):
        pass
    
    assert final_facts >= 8, f"Expected at least 8 facts, got {final_facts}"
    


def test_rule_chaining():
    """
    TEST: Verify rules trigger other rules (cascading inference)
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Chain Test User",
        allergies=["dairy"],
        dietary_restrictions=["vegetarian"],
        available_equipment=["oven"],
        skill_level="beginner"
    )
    
    recipe = Recipe(
        name="Cheese Pasta",
        ingredients=[
            Ingredient(name="pasta", quantity=200, unit="g"),
            Ingredient(name="cheese", quantity=100, unit="g", allergens=["dairy"])
        ],
        equipment=[Equipment(name="oven")],
        cuisine="Italian",
        diet="vegetarian"
    )
    
    
    
    recommended = engine.forward_chain(user, user, [recipe])
    
    
    
    categories = {
        'Allergy': [f for f in engine.working_memory if 'allergic' in f.lower()],
        'Diet': [f for f in engine.working_memory if 'diet' in f.lower() and 'allergic' not in f.lower()],
        'Equipment': [f for f in engine.working_memory if 'equipment' in f.lower()],
        'Skill': [f for f in engine.working_memory if 'skill' in f.lower()],
        'Budget': [f for f in engine.working_memory if 'budget' in f.lower()]
    }
    
    for category, facts in categories.items():
        if facts:
            for fact in facts[:3]:
                pass

    assert len([c for c in categories.values() if c]) >= 3, "Not enough fact categories - rules didn't cascade"
    


def test_comprehensive_scenario():
    """
    TEST: Comprehensive real-world scenario with multiple recipes
    """
    
    kb_path = Path(__file__).parent.parent / "inference" / "knowledge_base.yaml"
    engine = InferenceEngine(str(kb_path))
    
    user = User(
        name="Realistic User",
        allergies=["nuts"],
        dietary_restrictions=["vegetarian"],
        available_equipment=["oven", "pan", "blender"],
        skill_level="intermediate",
        budget=30.0,
        max_cooking_time=45
    )
    
    recipes = [
        Recipe(
            name="Almond Salad",
            ingredients=[Ingredient(name="almonds", quantity=50, unit="g", allergens=["nuts"])],
            cuisine="Healthy",
            diet="vegan",
            cost=8.0
        ),
        Recipe(
            name="Veggie Pasta",
            ingredients=[
                Ingredient(name="pasta", quantity=200, unit="g"),
                Ingredient(name="tomatoes", quantity=100, unit="g")
            ],
            equipment=[Equipment(name="pan")],
            cuisine="Italian",
            diet="vegetarian",
            skill="easy",
            cost=6.0
        ),
        Recipe(
            name="Beef Steak",
            ingredients=[Ingredient(name="beef", quantity=300, unit="g")],
            cuisine="American",
            diet="omnivore",
            cost=25.0
        ),
        Recipe(
            name="Mushroom Risotto",
            ingredients=[
                Ingredient(name="rice", quantity=200, unit="g"),
                Ingredient(name="mushrooms", quantity=150, unit="g")
            ],
            equipment=[Equipment(name="pan")],
            cuisine="Italian",
            diet="vegetarian",
            skill="medium",
            cost=12.0
        ),
        Recipe(
            name="Caesar Salad with Chicken",
            ingredients=[
                Ingredient(name="chicken", quantity=200, unit="g"),
                Ingredient(name="lettuce", quantity=100, unit="g")
            ],
            cuisine="American",
            diet="omnivore",
            cost=10.0
        )
    ]
    
    
    for i, recipe in enumerate(recipes, 1):
        diet_info = getattr(recipe, 'diet', 'unknown')
        allergens = set()
        for ing in recipe.ingredients:
            if hasattr(ing, 'allergens') and ing.allergens:
                allergens.update(ing.allergens)
        allergen_str = f" [{', '.join(allergens)}]" if allergens else ""
    
    recommended = engine.forward_chain(user, user, recipes)
    
    
    for i, fact in enumerate(sorted(engine.working_memory)[:15], 1):
        pass
    
    if len(engine.working_memory) > 15:
        pass

    assert len(engine.working_memory) >= 5, "Insufficient facts for comprehensive scenario"
    assert any('nut' in f.lower() for f in engine.working_memory), "Nut allergy not processed"
    assert any('vegetarian' in f.lower() or 'diet' in f.lower() for f in engine.working_memory), "Diet not processed"
    


def run_tests():
    """Run all comprehensive tests"""
    
    test_count = 0
    passed_count = 0
    
    tests = [
        ("Basic Fact Derivation", test_inference_derives_facts),
        ("Iterative Rule Firing", test_iterative_rule_firing),
        ("Allergy Detection", test_allergy_detection_and_exclusion),
        ("Equipment Compatibility", test_equipment_compatibility),
        ("Dietary Preferences", test_dietary_preferences),
        ("Skill Level Matching", test_skill_level_matching),
        ("Budget Constraints", test_budget_constraints),
        ("Working Memory", test_working_memory_accumulation),
        ("Rule Chaining", test_rule_chaining),
        ("Comprehensive Scenario", test_comprehensive_scenario)
    ]
    
    try:
        for name, test_func in tests:
            test_count += 1
            try:
                test_func()
                passed_count += 1
            except Exception as e:
                raise
        
        
    except AssertionError as e:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    run_tests()
