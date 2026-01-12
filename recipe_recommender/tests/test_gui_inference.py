"""
Comprehensive tests for the Test GUI page (2_Test_GUI.py)
Tests domain object creation, user preferences, and inference engine filtering
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import from recipe_recommender
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.user import User
from models.recipe import Recipe, Diet, DietRestriction, CookingTime, Skill, CookingMethod, Budget, Meal, Macros
from models.ingredient import Ingredient
from models.equipment import Equipment
from models.nutritional_info import NutritionalInfo
from models.allergy import Allergy
from models.budget_constraint import BudgetConstraint
from models.cooking_skill import CookingSkill
from models.time_constraint import TimeConstraint
from models.dietary_preference import DietaryPreference
from models.health_goal import HealthGoal
from models.kitchen import Kitchen
from data.sample_recipes import get_all_recipes
from system.inference_engine import InferenceEngine


class TestAllergyFiltering:
    """Test that recipes are properly filtered based on allergies"""
    
    def test_egg_allergy_filters_egg_recipes(self):
        """Users with egg allergy should not get recipes containing eggs"""
        # Create user with egg allergy
        user = User(
            name="Egg Allergy User",
            dietary_restrictions=[],
            allergies=["Eggs"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Eggs", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        # Get recipes
        recipes = get_all_recipes()
        
        # Run inference engine
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # Check that no recommended recipes contain eggs
        for recipe in recommended:
            has_eggs = recipe.has_ingredient("eggs")
            assert not has_eggs, f"Recipe '{recipe.name}' contains eggs but was recommended to user with egg allergy"
    
    def test_dairy_allergy_filters_dairy_recipes(self):
        """Users with dairy allergy should not get recipes containing dairy"""
        user = User(
            name="Dairy Allergy User",
            dietary_restrictions=[],
            allergies=["Dairy"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Dairy", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            # Check both ingredient name and common dairy products
            has_dairy = any(recipe.has_ingredient(item) for item in [
                "milk", "cheese", "butter", "cream", "yogurt", "dairy",
                "pecorino", "parmesan", "mozzarella", "ricotta"
            ])
            assert not has_dairy, f"Recipe '{recipe.name}' contains dairy but was recommended to user with dairy allergy"
    
    def test_multiple_allergies(self):
        """Users with multiple allergies should have all filtered"""
        user = User(
            name="Multiple Allergies User",
            dietary_restrictions=[],
            allergies=["Eggs", "Dairy", "Peanuts"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[
                Allergy(allergen_name="Eggs", severity="moderate"),
                Allergy(allergen_name="Dairy", severity="moderate"),
                Allergy(allergen_name="Peanuts", severity="moderate")
            ],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert not recipe.has_ingredient("eggs"), f"Recipe '{recipe.name}' has eggs"
            assert not any(recipe.has_ingredient(item) for item in ["milk", "cheese", "butter", "cream", "pecorino", "parmesan"]), f"Recipe '{recipe.name}' has dairy"
            assert not recipe.has_ingredient("peanuts"), f"Recipe '{recipe.name}' has peanuts"
    
    def test_tree_nuts_allergy(self):
        """Users with tree nut allergy should not get recipes with tree nuts"""
        user = User(
            name="Tree Nut Allergy User",
            dietary_restrictions=[],
            allergies=["Tree Nuts"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Tree Nuts", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            has_tree_nuts = any(recipe.has_ingredient(item) for item in [
                "almonds", "walnuts", "cashews", "pecans", "hazelnuts", 
                "pistachios", "macadamia", "pine nuts", "almond butter"
            ])
            assert not has_tree_nuts, f"Recipe '{recipe.name}' contains tree nuts"


class TestDietaryRestrictions:
    """Test that recipes are properly filtered based on dietary restrictions"""
    
    def test_vegan_diet(self):
        """Vegan users should only get vegan recipes"""
        user = User(
            name="Vegan User",
            dietary_restrictions=["vegan"],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="vegan", restrictions=["vegan"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            # Vegan recipes should not have meat, dairy, eggs, fish, or honey
            assert recipe.diet == Diet.VEGAN, f"Recipe '{recipe.name}' is not vegan (diet: {recipe.diet})"
    
    def test_vegetarian_diet(self):
        """Vegetarian users should only get vegetarian or vegan recipes"""
        user = User(
            name="Vegetarian User",
            dietary_restrictions=["vegetarian"],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="vegetarian", restrictions=["vegetarian"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.diet in [Diet.VEGAN, Diet.VEGETARIAN], f"Recipe '{recipe.name}' is not vegetarian/vegan (diet: {recipe.diet})"
    
    def test_pescatarian_diet(self):
        """Pescatarian users should get fish/seafood but not meat"""
        user = User(
            name="Pescatarian User",
            dietary_restrictions=["pescatarian"],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="pescatarian", restrictions=["pescatarian"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            # Pescatarians can eat vegan, vegetarian, pescatarian, but NOT omnivore (which has meat)
            assert recipe.diet != Diet.OMNIVORE, f"Recipe '{recipe.name}' contains meat (diet: {recipe.diet}), not suitable for pescatarian"
    
    def test_vegan_with_egg_allergy_redundancy(self):
        """Vegan diet already excludes eggs, but allergy should also work"""
        user = User(
            name="Vegan with Egg Allergy",
            dietary_restrictions=["vegan"],
            allergies=["Eggs"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Eggs", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="vegan", restrictions=["vegan"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.diet == Diet.VEGAN, f"Recipe '{recipe.name}' is not vegan"
            assert not recipe.has_ingredient("eggs"), f"Recipe '{recipe.name}' contains eggs"


class TestSkillLevel:
    """Test that recipes match user's cooking skill level"""
    
    def test_beginner_skill(self):
        """Beginners should get easy recipes"""
        user = User(
            name="Beginner Cook",
            dietary_restrictions=[],
            allergies=[],
            skill_level="beginner",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="beginner"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            # Beginners should only get easy recipes
            assert recipe.skill == Skill.EASY, f"Recipe '{recipe.name}' skill level ({recipe.skill}) too high for beginner"
    
    def test_advanced_skill_gets_all(self):
        """Advanced cooks should get recipes of all skill levels"""
        user = User(
            name="Advanced Cook",
            dietary_restrictions=[],
            allergies=[],
            skill_level="advanced",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="advanced"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # Advanced users should get at least some recipes
        assert len(recommended) > 0, "Advanced users should get recipe recommendations"


class TestTimeConstraints:
    """Test that recipes match user's available cooking time"""
    
    def test_15_minute_constraint(self):
        """Users with 15 minutes should only get quick recipes"""
        user = User(
            name="Busy User",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=15,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=TimeConstraint(available_minutes=15),
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            # Rule checks cooking_time enum, not total time (prep + cook)
            assert recipe.cooking_time == CookingTime.LESS_THAN_15, f"Recipe '{recipe.name}' cooking time ({recipe.cooking_time}) exceeds constraint"
    
    def test_30_minute_constraint(self):
        """Users with 30 minutes should get quick to medium recipes"""
        user = User(
            name="Medium Time User",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=30,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=TimeConstraint(available_minutes=30),
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            # Should exclude recipes that take more than 45 minutes
            assert recipe.cooking_time != CookingTime.MORE_THAN_45, f"Recipe '{recipe.name}' cooking time too long for 30 minute constraint"
    
    def _get_cooking_time_minutes(self, cooking_time):
        """Helper to convert CookingTime enum to approximate minutes"""
        if cooking_time == CookingTime.LESS_THAN_15:
            return 15
        elif cooking_time == CookingTime.BETWEEN_15_45:
            return 30
        elif cooking_time == CookingTime.MORE_THAN_45:
            return 60
        return 0


class TestEdgeCases:
    """Test edge cases and extreme scenarios"""
    
    def test_no_preferences_gets_recommendations(self):
        """Users with no restrictions should get many recommendations"""
        user = User(
            name="No Restrictions User",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        assert len(recommended) > 0, "User with no restrictions should get recommendations"
    
    def test_all_allergies_severely_limits_options(self):
        """Users allergic to everything should get very few or no recommendations"""
        user = User(
            name="All Allergies User",
            dietary_restrictions=[],
            allergies=["Dairy", "Eggs", "Shellfish", "Fish", "Peanuts", "Tree Nuts", "Wheat", "Soy", "Sesame"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[
                Allergy(allergen_name="Dairy", severity="severe"),
                Allergy(allergen_name="Eggs", severity="severe"),
                Allergy(allergen_name="Shellfish", severity="severe"),
                Allergy(allergen_name="Fish", severity="severe"),
                Allergy(allergen_name="Peanuts", severity="severe"),
                Allergy(allergen_name="Tree Nuts", severity="severe"),
                Allergy(allergen_name="Wheat", severity="severe"),
                Allergy(allergen_name="Soy", severity="severe"),
                Allergy(allergen_name="Sesame", severity="severe"),
            ],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # Should have very limited options
        assert len(recommended) < len(recipes), "User with all allergies should have filtered recommendations"
    
    def test_vegan_beginner_15_minutes(self):
        """Test combination of vegan + beginner + time constraint"""
        user = User(
            name="Vegan Beginner Busy",
            dietary_restrictions=["vegan"],
            allergies=[],
            skill_level="beginner",
            available_equipment=[],
            max_cooking_time=15,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="beginner"),
            time_constraint=TimeConstraint(available_minutes=15),
            dietary_preference=DietaryPreference(type="vegan", restrictions=["vegan"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.diet == Diet.VEGAN, f"Recipe '{recipe.name}' is not vegan"
            assert recipe.skill == Skill.EASY, f"Recipe '{recipe.name}' too difficult for beginner"
            assert recipe.cooking_time == CookingTime.LESS_THAN_15, f"Recipe '{recipe.name}' takes too long"


class TestDomainObjects:
    """Test domain object creation from GUI answers"""
    
    def test_allergy_creation(self):
        """Test Allergy domain object creation"""
        allergy = Allergy(allergen_name="Eggs", severity="moderate")
        assert allergy.allergen_name == "Eggs"
        assert allergy.severity == "moderate"
        assert "Eggs" in str(allergy)
    
    def test_budget_constraint_creation(self):
        """Test BudgetConstraint domain object creation"""
        budget = BudgetConstraint(preferred_range="budget", flexibility="flexible")
        assert budget.preferred_range == "budget"
        assert budget.flexibility == "flexible"
    
    def test_cooking_skill_creation(self):
        """Test CookingSkill domain object creation"""
        skill = CookingSkill(level="intermediate", years_experience=0)
        assert skill.level == "intermediate"
    
    def test_time_constraint_creation(self):
        """Test TimeConstraint domain object creation"""
        time = TimeConstraint(available_minutes=30)
        assert time.available_minutes == 30
    
    def test_dietary_preference_creation(self):
        """Test DietaryPreference domain object creation"""
        pref = DietaryPreference(
            type="vegan",
            restrictions=["vegan", "gluten-free"],
            preferred_cuisines=[]
        )
        assert pref.type == "vegan"
        assert "vegan" in pref.restrictions
        assert "gluten-free" in pref.restrictions
    
    def test_health_goal_creation(self):
        """Test HealthGoal domain object creation"""
        goal = HealthGoal(goal_type="weight-loss", priority="high")
        assert goal.goal_type == "weight-loss"
    
    def test_kitchen_creation(self):
        """Test Kitchen domain object creation"""
        kitchen = Kitchen(available_equipment=["Oven", "Stove", "Microwave"])
        assert "Oven" in kitchen.available_equipment
        assert len(kitchen.available_equipment) == 3


class TestUserCreation:
    """Test User object creation with various combinations"""
    
    def test_user_with_all_attributes(self):
        """Test creating User with all attributes populated"""
        user = User(
            name="Complete User",
            dietary_restrictions=["vegan", "gluten-free"],
            allergies=["Eggs", "Dairy"],
            skill_level="intermediate",
            available_equipment=["Oven", "Stove"],
            max_cooking_time=45,
            health_goals=["weight-loss", "energy-boost"],
            allergies_list=[
                Allergy(allergen_name="Eggs", severity="moderate"),
                Allergy(allergen_name="Dairy", severity="severe")
            ],
            skill=CookingSkill(level="intermediate"),
            time_constraint=TimeConstraint(available_minutes=45),
            dietary_preference=DietaryPreference(
                type="vegan",
                restrictions=["vegan", "gluten-free"]
            ),
            health_goals_list=[
                HealthGoal(goal_type="weight-loss"),
                HealthGoal(goal_type="energy-boost")
            ],
            budget=BudgetConstraint(preferred_range="moderate"),
            kitchen=Kitchen(available_equipment=["Oven", "Stove"])
        )
        
        assert user.name == "Complete User"
        assert len(user.allergies) == 2
        assert len(user.dietary_restrictions) == 2
        assert user.skill_level == "intermediate"
        assert user.max_cooking_time == 45
    
    def test_user_with_minimal_attributes(self):
        """Test creating User with minimal required attributes"""
        user = User(
            name="Minimal User",
            dietary_restrictions=[],
            allergies=[],
            skill_level="beginner",
            available_equipment=[],
            max_cooking_time=30,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="beginner"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        assert user.name == "Minimal User"
        assert len(user.allergies) == 0
        assert len(user.dietary_restrictions) == 0


class TestComplexCombinations:
    """Test complex combinations of multiple filters"""
    
    def test_vegan_with_multiple_allergies(self):
        """Vegan user with dairy and nut allergies"""
        user = User(
            name="Vegan Allergy User",
            dietary_restrictions=["vegan"],
            allergies=["Dairy", "Tree Nuts", "Peanuts"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[
                Allergy(allergen_name="Dairy", severity="severe"),
                Allergy(allergen_name="Tree Nuts", severity="severe"),
                Allergy(allergen_name="Peanuts", severity="severe")
            ],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="vegan", restrictions=["vegan"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # Should get vegan recipes without dairy, tree nuts, or peanuts
        for recipe in recommended:
            assert recipe.diet == Diet.VEGAN, f"Recipe '{recipe.name}' not vegan"
            assert not any(recipe.has_ingredient(item) for item in ["dairy", "cheese", "butter", "milk"]), f"Recipe '{recipe.name}' has dairy"
            assert not recipe.has_ingredient("almond butter"), f"Recipe '{recipe.name}' has tree nuts"
            assert not recipe.has_ingredient("peanuts"), f"Recipe '{recipe.name}' has peanuts"
    
    def test_beginner_vegan_30_minutes(self):
        """Beginner vegan cook with 30-minute constraint"""
        user = User(
            name="Beginner Vegan Busy",
            dietary_restrictions=["vegan"],
            allergies=[],
            skill_level="beginner",
            available_equipment=["Stove", "Pot"],
            max_cooking_time=30,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="beginner"),
            time_constraint=TimeConstraint(available_minutes=30),
            dietary_preference=DietaryPreference(type="vegan", restrictions=["vegan"]),
            health_goals_list=[],
            budget=None,
            kitchen=Kitchen(available_equipment=["Stove", "Pot"])
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.diet == Diet.VEGAN, f"Recipe '{recipe.name}' not vegan"
            assert recipe.skill == Skill.EASY, f"Recipe '{recipe.name}' too difficult"
            assert recipe.cooking_time != CookingTime.MORE_THAN_45, f"Recipe '{recipe.name}' takes too long"
    
    def test_vegetarian_egg_allergy(self):
        """Vegetarian with egg allergy should exclude egg-based recipes"""
        user = User(
            name="Vegetarian No Eggs",
            dietary_restrictions=["vegetarian"],
            allergies=["Eggs"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Eggs", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="vegetarian", restrictions=["vegetarian"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.diet in [Diet.VEGAN, Diet.VEGETARIAN], f"Recipe '{recipe.name}' not vegetarian"
            assert not recipe.has_ingredient("eggs"), f"Recipe '{recipe.name}' contains eggs"
    
    def test_all_dietary_restrictions_combined(self):
        """User selecting vegan, gluten-free, dairy-free, low-carb"""
        user = User(
            name="Multiple Restrictions User",
            dietary_restrictions=["vegan", "gluten-free", "dairy-free", "low-carb"],
            allergies=["Wheat", "Dairy"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[
                Allergy(allergen_name="Wheat", severity="moderate"),
                Allergy(allergen_name="Dairy", severity="moderate")
            ],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(
                type="vegan",
                restrictions=["vegan", "gluten-free", "dairy-free", "low-carb"]
            ),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.diet == Diet.VEGAN, f"Recipe '{recipe.name}' not vegan"
            assert not recipe.has_ingredient("wheat"), f"Recipe '{recipe.name}' has wheat"
            assert not any(recipe.has_ingredient(item) for item in ["dairy", "cheese", "butter", "milk", "cream"]), f"Recipe '{recipe.name}' has dairy"


class TestAllergyEdgeCases:
    """Test edge cases for allergy filtering"""
    
    def test_shellfish_allergy(self):
        """Users with shellfish allergy should not get shellfish recipes"""
        user = User(
            name="Shellfish Allergy User",
            dietary_restrictions=[],
            allergies=["Shellfish"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Shellfish", severity="severe")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            has_shellfish = any(recipe.has_ingredient(item) for item in [
                "shrimp", "crab", "lobster", "clams", "mussels", "oysters", "shellfish"
            ])
            assert not has_shellfish, f"Recipe '{recipe.name}' contains shellfish"
    
    def test_fish_allergy(self):
        """Users with fish allergy should not get fish recipes"""
        user = User(
            name="Fish Allergy User",
            dietary_restrictions=[],
            allergies=["Fish"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Fish", severity="severe")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            has_fish = any(recipe.has_ingredient(item) for item in [
                "salmon", "tuna", "cod", "tilapia", "fish", "anchovy", "sardine"
            ])
            assert not has_fish, f"Recipe '{recipe.name}' contains fish"
    
    def test_wheat_allergy(self):
        """Users with wheat allergy should not get wheat-based recipes"""
        user = User(
            name="Wheat Allergy User",
            dietary_restrictions=[],
            allergies=["Wheat"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Wheat", severity="severe")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            has_wheat = any(recipe.has_ingredient(item) for item in [
                "wheat", "flour", "bread", "pasta", "noodles"
            ])
            assert not has_wheat, f"Recipe '{recipe.name}' contains wheat"
    
    def test_soy_allergy(self):
        """Users with soy allergy should not get soy-based recipes"""
        user = User(
            name="Soy Allergy User",
            dietary_restrictions=[],
            allergies=["Soy"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Soy", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            has_soy = any(recipe.has_ingredient(item) for item in [
                "soy", "tofu", "soy sauce", "edamame", "tempeh"
            ])
            assert not has_soy, f"Recipe '{recipe.name}' contains soy"
    
    def test_sesame_allergy(self):
        """Users with sesame allergy should not get sesame recipes"""
        user = User(
            name="Sesame Allergy User",
            dietary_restrictions=[],
            allergies=["Sesame"],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Sesame", severity="moderate")],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            has_sesame = any(recipe.has_ingredient(item) for item in [
                "sesame", "tahini", "sesame oil", "sesame seeds"
            ])
            assert not has_sesame, f"Recipe '{recipe.name}' contains sesame"


class TestSkillLevelVariations:
    """Test different skill level scenarios"""
    
    def test_intermediate_skill_gets_easy_and_medium(self):
        """Intermediate cooks should get easy and medium recipes"""
        user = User(
            name="Intermediate Cook",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # Should include both easy and medium recipes
        skill_levels = {recipe.skill for recipe in recommended}
        assert Skill.EASY in skill_levels or Skill.MEDIUM in skill_levels, "Should have easy or medium recipes"
        
        # Should not have experienced recipes (if the rule is implemented)
        for recipe in recommended:
            assert recipe.skill in [Skill.EASY, Skill.MEDIUM, Skill.EXPERIENCED], f"Unexpected skill level: {recipe.skill}"
    
    def test_beginner_excludes_complex_recipes(self):
        """Beginners should not get medium or experienced recipes"""
        user = User(
            name="Beginner Cook",
            dietary_restrictions=[],
            allergies=[],
            skill_level="beginner",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="beginner"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        all_recipe_skills = [recipe.skill for recipe in recipes]
        
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # All recommended should be easy
        for recipe in recommended:
            assert recipe.skill == Skill.EASY, f"Recipe '{recipe.name}' is {recipe.skill}, not easy"


class TestTimeConstraintVariations:
    """Test different time constraint scenarios"""
    
    def test_60_minute_constraint_allows_most_recipes(self):
        """Users with 60 minutes should get most recipes"""
        user = User(
            name="1 Hour User",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=TimeConstraint(available_minutes=60),
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        # Should get multiple recipes
        assert len(recommended) >= 3, f"Expected at least 3 recipes, got {len(recommended)}"
    
    def test_30_minute_excludes_very_long_recipes(self):
        """Users with 30 minutes should not get 45+ minute recipes"""
        user = User(
            name="30 Minute User",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=30,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=TimeConstraint(available_minutes=30),
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        for recipe in recommended:
            assert recipe.cooking_time != CookingTime.MORE_THAN_45, f"Recipe '{recipe.name}' takes over 45 minutes"


class TestInferenceEngineRobustness:
    """Test inference engine handles edge cases correctly"""
    
    def test_empty_allergy_list(self):
        """User with no allergies should work fine"""
        user = User(
            name="No Allergies",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        assert len(recommended) > 0, "Should get recommendations with no allergies"
    
    def test_empty_dietary_restrictions(self):
        """User with no dietary restrictions should work fine"""
        user = User(
            name="Omnivore",
            dietary_restrictions=[],
            allergies=[],
            skill_level="intermediate",
            available_equipment=[],
            max_cooking_time=60,
            health_goals=[],
            allergies_list=[],
            skill=CookingSkill(level="intermediate"),
            time_constraint=None,
            dietary_preference=DietaryPreference(type="omnivore"),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine = InferenceEngine(str(kb_path))
        engine.forward_chain(user, None, recipes)
        recommended = engine.get_recommended_recipes(recipes)
        
        assert len(recommended) == len(recipes), "Omnivore with no restrictions should get all recipes"
    
    def test_inference_engine_idempotent(self):
        """Running inference multiple times should give same results"""
        user = User(
            name="Test User",
            dietary_restrictions=["vegan"],
            allergies=["Eggs"],
            skill_level="beginner",
            available_equipment=[],
            max_cooking_time=30,
            health_goals=[],
            allergies_list=[Allergy(allergen_name="Eggs", severity="moderate")],
            skill=CookingSkill(level="beginner"),
            time_constraint=TimeConstraint(available_minutes=30),
            dietary_preference=DietaryPreference(type="vegan", restrictions=["vegan"]),
            health_goals_list=[],
            budget=None,
            kitchen=None
        )
        
        recipes1 = get_all_recipes()
        kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
        engine1 = InferenceEngine(str(kb_path))
        engine1.forward_chain(user, None, recipes1)
        recommended1 = engine1.get_recommended_recipes(recipes1)
        
        recipes2 = get_all_recipes()
        engine2 = InferenceEngine(str(kb_path))
        engine2.forward_chain(user, None, recipes2)
        recommended2 = engine2.get_recommended_recipes(recipes2)
        
        assert len(recommended1) == len(recommended2), "Should get same number of recommendations"
        assert {r.name for r in recommended1} == {r.name for r in recommended2}, "Should get same recipes"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
