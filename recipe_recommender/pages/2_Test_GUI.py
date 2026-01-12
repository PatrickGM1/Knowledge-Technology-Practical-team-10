import streamlit as st
from pathlib import Path
from models import (
    Recipe, Diet, DietRestriction, CookingTime, 
    Skill, CookingMethod, Budget, Meal, Macros
)
from models.allergy import Allergy
from models.budget_constraint import BudgetConstraint
from models.cooking_skill import CookingSkill
from models.time_constraint import TimeConstraint
from models.dietary_preference import DietaryPreference
from models.health_goal import HealthGoal
from models.kitchen import Kitchen
from data.sample_recipes import get_all_recipes

st.set_page_config(
    page_title="Test Domain Objects",
    layout="wide"
)

st.title("🧪 Test All Domain Objects")
st.write("Answer the questions one at a time to see all domain objects being created!")
st.divider()

# All quiz questions (text, category, value, question type)
QUESTIONS = [
    # Allergens - can select multiple
    ("Are you allergic to Dairy?", "allergens", "Dairy", "multiple"),
    ("Are you allergic to Eggs?", "allergens", "Eggs", "multiple"),
    ("Are you allergic to Shellfish?", "allergens", "Shellfish", "multiple"),
    ("Are you allergic to Fish?", "allergens", "Fish", "multiple"),
    ("Are you allergic to Peanuts?", "allergens", "Peanuts", "multiple"),
    ("Are you allergic to Tree Nuts?", "allergens", "Tree Nuts", "multiple"),
    ("Are you allergic to Wheat?", "allergens", "Wheat", "multiple"),
    ("Are you allergic to Soy?", "allergens", "Soy", "multiple"),
    ("Are you allergic to Sesame?", "allergens", "Sesame", "multiple"),
    
    # Budget - special three-button layout
    ("What's your budget for ingredients?", "budget", "budget", "budget"),
    
    # Skill level - special three-button layout
    ("What's your cooking experience?", "skill", "intermediate", "skill"),
    
    # Time - special three-button layout
    ("How much time can you spend cooking?", "time", 30, "time"),
    
    # Dietary preferences - can select multiple
    ("Do you follow a Vegan diet?", "dietary_prefs", "vegan", "multiple"),
    ("Do you follow a Vegetarian diet?", "dietary_prefs", "vegetarian", "multiple"),
    ("Do you need Gluten-Free options?", "dietary_prefs", "gluten-free", "multiple"),
    ("Do you need Dairy-Free options?", "dietary_prefs", "dairy-free", "multiple"),
    ("Are you looking for Low-Carb recipes?", "dietary_prefs", "low-carb", "multiple"),
    ("Are you looking for High-Protein recipes?", "dietary_prefs", "high-protein", "multiple"),
    ("Do you eat fish but not meat? (Pescatarian)", "dietary_prefs", "pescatarian", "multiple"),
    
    # Health goals - can select multiple
    ("Is Weight Loss one of your goals?", "health_goals", "weight-loss", "multiple"),
    ("Is Muscle Gain one of your goals?", "health_goals", "muscle-gain", "multiple"),
    ("Is Heart Health one of your goals?", "health_goals", "heart-health", "multiple"),
    ("Do you need to control Blood Sugar?", "health_goals", "blood-sugar-control", "multiple"),
    ("Are you looking for an Energy Boost?", "health_goals", "energy-boost", "multiple"),
    
    # Kitchen equipment - can select multiple
    ("Do you have an Oven?", "equipment", "Oven", "multiple"),
    ("Do you have a Stove?", "equipment", "Stove", "multiple"),
    ("Do you have a Microwave?", "equipment", "Microwave", "multiple"),
    ("Do you have a Blender?", "equipment", "Blender", "multiple"),
    ("Do you have a Food Processor?", "equipment", "Food Processor", "multiple"),
    ("Do you have an Air Fryer?", "equipment", "Air Fryer", "multiple"),
    ("Do you have a Slow Cooker?", "equipment", "Slow Cooker", "multiple"),
    ("Do you have a Grill?", "equipment", "Grill", "multiple"),
]

# Track quiz progress
if 'test_current_question' not in st.session_state:
    st.session_state.test_current_question = 0
    
if 'test_answers' not in st.session_state:
    st.session_state.test_answers = {
        'allergens': [],  # List of tuples: (allergen_name, severity)
        'budget': [],  # Will have 1 item: (min, max)
        'skill': [],  # Will have 1 item: SkillLevel
        'time': [],  # Will have 1 item: minutes
        'dietary_prefs': [],  # List of PreferenceType
        'health_goals': [],  # List of GoalType
        'equipment': []  # List of equipment names
    }

if 'test_quiz_complete' not in st.session_state:
    st.session_state.test_quiz_complete = False


def answer_question(answer, custom_value=None):
    """Process user's answer and advance to next question"""
    question_text, category, value, q_type = QUESTIONS[st.session_state.test_current_question]
    
    if custom_value is not None:
        # Budget/skill/time questions use custom value
        if answer:
            st.session_state.test_answers[category].append(custom_value)
    else:
        if answer:
            # For allergens, also need severity
            if category == "allergens":
                severity = "moderate"  # Default severity: mild, moderate, or severe
                st.session_state.test_answers[category].append((value, severity))
            else:
                st.session_state.test_answers[category].append(value)
    
    st.session_state.test_current_question += 1
    
    # Quiz finished?
    if st.session_state.test_current_question >= len(QUESTIONS):
        st.session_state.test_quiz_complete = True

def reset_quiz():
    """Clear all answers and restart from beginning"""
    st.session_state.test_current_question = 0
    st.session_state.test_answers = {
        'allergens': [],
        'budget': [],
        'skill': [],
        'time': [],
        'dietary_prefs': [],
        'health_goals': [],
        'equipment': []
    }
    st.session_state.test_quiz_complete = False

# Show quiz questions
if not st.session_state.test_quiz_complete:
    progress = st.session_state.test_current_question / len(QUESTIONS)
    st.progress(progress)
    st.write(f"Question {st.session_state.test_current_question + 1} of {len(QUESTIONS)}")
    
    st.divider()
    
    question_text, category, value, q_type = QUESTIONS[st.session_state.test_current_question]
    st.subheader(question_text)
    
    # Budget question gets three buttons
    if q_type == "budget":
        st.markdown("""
            <style>
                div.stButton > button[kind="primary"] {
                    background-color: transparent;
                    color: #28a745;
                    border: 2px solid #28a745;
                }
                div.stButton > button[kind="primary"]:hover {
                    background-color: #28a745;
                    color: white;
                    border: 2px solid #28a745;
                }   
                div.stButton > button[kind="secondary"] {
                    background-color: transparent;
                    color: #007bff;
                    border: 2px solid #007bff;
                }
                div.stButton > button[kind="secondary"]:hover {
                    background-color: #007bff;
                    color: white;
                    border: 2px solid #007bff;
                }
                div.stButton > button[kind="tertiary"] {
                    background-color: transparent;
                    color: #dc3545;
                    border: 2px solid #dc3545;
                }
                div.stButton > button[kind="tertiary"]:hover {
                    background-color: #dc3545;
                    color: white;
                    border: 2px solid #dc3545;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Budget\n(Low Cost)", key=f"budget_low_{st.session_state.test_current_question}", use_container_width=True, type="secondary"):
                answer_question(True, "budget")
                st.rerun()
        
        with col2:
            if st.button("Moderate\n(Average Cost)", key=f"budget_mid_{st.session_state.test_current_question}", use_container_width=True, type="primary"):
                answer_question(True, "moderate")
                st.rerun()
        
        with col3:
            if st.button("Premium\n(Higher Cost)", key=f"budget_high_{st.session_state.test_current_question}", use_container_width=True, type="tertiary"):
                answer_question(True, "premium")
                st.rerun()
    
    # Skill question gets three buttons: Beginner/Intermediate/Advanced
    elif q_type == "skill":
        st.markdown("""
            <style>
                div.stButton > button[kind="primary"] {
                    background-color: transparent;
                    color: #28a745;
                    border: 2px solid #28a745;
                }
                div.stButton > button[kind="primary"]:hover {
                    background-color: #28a745;
                    color: white;
                    border: 2px solid #28a745;
                }   
                div.stButton > button[kind="secondary"] {
                    background-color: transparent;
                    color: #007bff;
                    border: 2px solid #007bff;
                }
                div.stButton > button[kind="secondary"]:hover {
                    background-color: #007bff;
                    color: white;
                    border: 2px solid #007bff;
                }
                div.stButton > button[kind="tertiary"] {
                    background-color: transparent;
                    color: #dc3545;
                    border: 2px solid #dc3545;
                }
                div.stButton > button[kind="tertiary"]:hover {
                    background-color: #dc3545;
                    color: white;
                    border: 2px solid #dc3545;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Beginner", key=f"skill_beginner_{st.session_state.test_current_question}", use_container_width=True, type="secondary"):
                answer_question(True, "beginner")
                st.rerun()
        
        with col2:
            if st.button("Intermediate", key=f"skill_intermediate_{st.session_state.test_current_question}", use_container_width=True, type="primary"):
                answer_question(True, "intermediate")
                st.rerun()
        
        with col3:
            if st.button("Advanced", key=f"skill_advanced_{st.session_state.test_current_question}", use_container_width=True, type="tertiary"):
                answer_question(True, "advanced")
                st.rerun()
    
    # Time question gets three buttons
    elif q_type == "time":
        st.markdown("""
            <style>
                div.stButton > button[kind="primary"] {
                    background-color: transparent;
                    color: #28a745;
                    border: 2px solid #28a745;
                }
                div.stButton > button[kind="primary"]:hover {
                    background-color: #28a745;
                    color: white;
                    border: 2px solid #28a745;
                }
                div.stButton > button[kind="secondary"] {
                    background-color: transparent;
                    color: #007bff;
                    border: 2px solid #007bff;
                }
                div.stButton > button[kind="secondary"]:hover {
                    background-color: #007bff;
                    color: white;
                    border: 2px solid #007bff;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("< 15 min", key=f"time_less_{st.session_state.test_current_question}", use_container_width=True, type="secondary"):
                answer_question(True, 15)
                st.rerun()
        
        with col2:
            if st.button("15-45 min", key=f"time_yes_{st.session_state.test_current_question}", use_container_width=True, type="primary"):
                answer_question(True, 30)
                st.rerun()
        
        with col3:
            if st.button("> 45 min", key=f"time_more_{st.session_state.test_current_question}", use_container_width=True, type="secondary"):
                answer_question(True, 60)
                st.rerun()
    
    # All other questions get yes/no buttons
    else:
        st.markdown("""
            <style>
                div.stButton > button[kind="primary"] {
                    background-color: transparent;
                    color: #28a745;
                    border: 2px solid #28a745;
                }
                div.stButton > button[kind="primary"]:hover {
                    background-color: #28a745;
                    color: white;
                    border: 2px solid #28a745;
                }
                div.stButton > button[kind="secondary"] {
                    background-color: transparent;
                    color: #dc3545;
                    border: 2px solid #dc3545;
                }
                div.stButton > button[kind="secondary"]:hover {
                    background-color: #dc3545;
                    color: white;
                    border: 2px solid #dc3545;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Yes", key=f"yes_{st.session_state.test_current_question}", use_container_width=True, type="primary"):
                answer_question(True)
                st.rerun()
        
        with col2:
            if st.button("No", key=f"no_{st.session_state.test_current_question}", use_container_width=True, type="secondary"):
                answer_question(False)
                st.rerun()
    
    st.divider()
    
    if st.button("🔄 Reset Quiz", key=f"reset_btn_{st.session_state.test_current_question}", use_container_width=False):
        reset_quiz()
        st.rerun()

else:
    # Quiz complete - show all created domain objects
    st.success("✅ Quiz Complete! Here are all your domain objects:")
    st.divider()
    
    # Display all created domain objects
    st.subheader("📋 Created Domain Objects")
    
    # Allergies
    if st.session_state.test_answers['allergens']:
        st.markdown("### 🚫 Allergies")
        for allergen_name, severity in st.session_state.test_answers['allergens']:
            st.write(f"- {allergen_name}")
    else:
        st.info("No allergies selected")
    
    # Budget Constraint
    if st.session_state.test_answers['budget']:
        st.markdown("### 💰 Budget Constraint")
        budget_pref = st.session_state.test_answers['budget'][0]
        budget = BudgetConstraint(preferred_range=budget_pref, flexibility='flexible')
        st.write(f"- {budget}")
    else:
        st.info("No budget selected")
    
    # Cooking Skill
    if st.session_state.test_answers['skill']:
        st.markdown("### 👨‍🍳 Cooking Skill")
        skill_level = st.session_state.test_answers['skill'][0]
        skill = CookingSkill(skill_level)
        st.write(f"- {skill}")
    else:
        st.info("No skill level selected")
    
    # Time Constraint
    if st.session_state.test_answers['time']:
        st.markdown("### ⏰ Time Constraint")
        time_minutes = st.session_state.test_answers['time'][0]
        time = TimeConstraint(time_minutes)
        st.write(f"- {time}")
    else:
        st.info("No time constraint selected")
    
    # Dietary Preferences
    if st.session_state.test_answers['dietary_prefs']:
        st.markdown("### 🥗 Dietary Preferences")
        for pref_type in st.session_state.test_answers['dietary_prefs']:
            pref = DietaryPreference(type=pref_type)
            st.write(f"- {pref}")
    else:
        st.info("No dietary preferences selected")
    
    # Health Goals
    if st.session_state.test_answers['health_goals']:
        st.markdown("### 🎯 Health Goals")
        for goal_type in st.session_state.test_answers['health_goals']:
            goal = HealthGoal(goal_type=goal_type)
            st.write(f"- {goal}")
    else:
        st.info("No health goals selected")
    
    # Kitchen Equipment
    if st.session_state.test_answers['equipment']:
        st.markdown("### 🔧 Kitchen Equipment")
        kitchen = Kitchen(st.session_state.test_answers['equipment'])
        st.write(f"- {kitchen}")
        st.write(f"  Available equipment: {', '.join(st.session_state.test_answers['equipment'])}")
    else:
        st.info("No equipment selected")
    
    st.divider()
    
    # Create User object and get recipe recommendations
    st.subheader("🍽️ Your Recipe Recommendations")
    
    from models.user import User
    from system.inference_engine import InferenceEngine
    
    # Create domain objects for User
    allergies_list = [Allergy(allergen_name=a, severity=s) for a, s in st.session_state.test_answers['allergens']]
    
    skill_obj = CookingSkill(level=st.session_state.test_answers['skill'][0] if st.session_state.test_answers['skill'] else 'beginner')
    
    time_obj = TimeConstraint(
        available_minutes=st.session_state.test_answers['time'][0] if st.session_state.test_answers['time'] else 60
    ) if st.session_state.test_answers['time'] else None
    
    dietary_prefs_list = [DietaryPreference(type=p) for p in st.session_state.test_answers['dietary_prefs']]
    
    health_goals_list = [HealthGoal(goal_type=g) for g in st.session_state.test_answers['health_goals']]
    
    budget_obj = BudgetConstraint(
        preferred_range=st.session_state.test_answers['budget'][0] if st.session_state.test_answers['budget'] else 'moderate',
        flexibility='flexible'
    ) if st.session_state.test_answers['budget'] else None
    
    kitchen_obj = Kitchen(
        available_equipment=st.session_state.test_answers['equipment']
    ) if st.session_state.test_answers['equipment'] else None
    
    # Build dietary restrictions list from preferences for legacy compatibility
    dietary_restrictions_list = []
    for pref in st.session_state.test_answers['dietary_prefs']:
        dietary_restrictions_list.append(pref)
    
    # Determine primary diet type for dietary_preference
    diet_type = 'omnivore'
    if 'vegan' in st.session_state.test_answers['dietary_prefs']:
        diet_type = 'vegan'
    elif 'vegetarian' in st.session_state.test_answers['dietary_prefs']:
        diet_type = 'vegetarian'
    elif 'pescatarian' in st.session_state.test_answers['dietary_prefs']:
        diet_type = 'pescatarian'
    
    primary_dietary_pref = DietaryPreference(
        type=diet_type,
        restrictions=dietary_restrictions_list,
        preferred_cuisines=[]
    )
    
    # Create User object
    user = User(
        name="Test User",
        dietary_restrictions=dietary_restrictions_list,
        allergies=[a for a, _ in st.session_state.test_answers['allergens']],
        skill_level=st.session_state.test_answers['skill'][0] if st.session_state.test_answers['skill'] else 'beginner',
        available_equipment=st.session_state.test_answers['equipment'],
        max_cooking_time=st.session_state.test_answers['time'][0] if st.session_state.test_answers['time'] else 60,
        health_goals=st.session_state.test_answers['health_goals'],
        allergies_list=allergies_list,
        skill=skill_obj,
        time_constraint=time_obj,
        dietary_preference=primary_dietary_pref,
        health_goals_list=health_goals_list,
        budget=budget_obj,
        kitchen=kitchen_obj
    )
    
    # Get all recipes
    all_recipes = get_all_recipes()
    
    # Run inference engine with knowledge base
    from pathlib import Path
    kb_path = Path(__file__).parent.parent / 'knowledge_base.yaml'
    
    engine = InferenceEngine(str(kb_path))
    engine.forward_chain(user, kitchen_obj, all_recipes)
    recommended = engine.get_recommended_recipes(all_recipes)
    
    if recommended:
        st.success(f"Found {len(recommended)} recipe(s) matching your preferences!")
        
        for recipe in recommended:
            with st.expander(f"📖 {recipe.name}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if recipe.description:
                        st.markdown(f"**{recipe.description}**")
                    
                    if recipe.prep_time:
                        st.write(f"⏱️ **Prep Time:** {recipe.prep_time} min")
                    st.write(f"🕐 **Cooking Time:** {recipe.cooking_time.value if hasattr(recipe.cooking_time, 'value') else recipe.cooking_time}")
                    st.write(f"👨‍🍳 **Skill Level:** {recipe.skill.value if hasattr(recipe.skill, 'value') else recipe.skill}")
                    st.write(f"🍽️ **Servings:** {recipe.servings}")
                    
                    if recipe.ingredients:
                        st.markdown("**Ingredients:**")
                        for ingredient in recipe.ingredients:
                            st.write(f"- {ingredient.quantity} {ingredient.unit} {ingredient.name}")
                    
                    if recipe.instructions:
                        st.markdown("**Instructions:**")
                        for i, instruction in enumerate(recipe.instructions, 1):
                            st.write(f"{i}. {instruction}")
                
                with col2:
                    if recipe.nutritional_info:
                        st.markdown("**Nutrition:**")
                        st.write(f"🔥 {recipe.nutritional_info.calories} cal")
                        st.write(f"🥩 {recipe.nutritional_info.protein}g protein")
                        st.write(f"🍞 {recipe.nutritional_info.carbohydrates}g carbs")
                        st.write(f"🧈 {recipe.nutritional_info.fat}g fat")
                    
                    if recipe.cost:
                        st.write(f"💰 **Cost:** €{recipe.cost:.2f}/serving")
    else:
        st.warning("No recipes match your criteria. Try adjusting your preferences!")
    
    st.divider()
    
    # Show raw session state for debugging
    with st.expander("🔍 View Raw Session State"):
        st.json(st.session_state.test_answers)
    
    # Reset button
    if st.button("🔄 Start Over", use_container_width=True, type="primary"):
        reset_quiz()
        st.rerun()
