"""
Recipe Recommender Streamlit UI
Forward-Chaining Inference System
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from constraints.user import User
from domainClasses.recipe import Recipe
from domainClasses.ingredient import Ingredient
from domainClasses.nutritional_info import NutritionalInfo
from inference.inference_engine import InferenceEngine
import yaml

st.set_page_config(
    page_title="Recipe Recommender - Forward-Chaining Inference",
    page_icon="🍳",
    layout="wide"
)

 # CSS for Streamlit buttons
st.markdown("""
    <style>
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }
        div.stButton > button[kind="primary"] {
            background-color: transparent;
            color: #28a745;
            border: 2px solid #28a745;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #28a745;
            color: white;
        }
        div.stButton > button[kind="secondary"] {
            background-color: transparent;
            color: #dc3545;
            border: 2px solid #dc3545;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #dc3545;
            color: white;
        }
        .stProgress > div > div {
            background-color: #28a745;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🍳 Recipe Recommender")
st.markdown("### *Powered by Forward-Chaining Inference Engine*")
st.write("Answer questions to find recipes that match your preferences!")
st.divider()

 # List of quiz questions. Some are conditional.
QUESTIONS = [
    # Gate questions - determine if we need to ask follow-ups
    ("Do you have any **food allergies**?", "has_allergies", True, "yes_no", None),
    
    # Allergy details (conditional - only if has_allergies)
    ("Are you allergic to **Dairy**?", "allergies", "dairy", "yes_no", lambda: st.session_state.answers.get('has_allergies') and 'vegan' not in st.session_state.answers.get('diet', [])),
    ("Are you allergic to **Eggs**?", "allergies", "eggs", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Shellfish**?", "allergies", "shellfish", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Fish**?", "allergies", "fish", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Peanuts**?", "allergies", "peanuts", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Tree Nuts**?", "allergies", "tree nuts", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Wheat/Gluten**?", "allergies", "gluten", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Soy**?", "allergies", "soy", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    ("Are you allergic to **Sesame**?", "allergies", "sesame", "yes_no", lambda: st.session_state.answers.get('has_allergies')),
    
    # Dietary preferences gate
    ("Do you follow any **special diet**? (vegan, vegetarian, pescatarian, etc.)", "has_special_diet", True, "yes_no", None),
    
    # Diet details (conditional) - with smart skipping
    ("Do you follow a **Vegan** diet?", "diet", "vegan", "yes_no", lambda: st.session_state.answers.get('has_special_diet')),
    ("Do you follow a **Vegetarian** diet?", "diet", "vegetarian", "yes_no", lambda: st.session_state.answers.get('has_special_diet') and 'vegan' not in st.session_state.answers.get('diet', [])),
    ("Do you eat **fish but not meat**? (Pescatarian)", "diet", "pescatarian", "yes_no", lambda: st.session_state.answers.get('has_special_diet') and 'vegan' not in st.session_state.answers.get('diet', []) and 'vegetarian' not in st.session_state.answers.get('diet', [])),
    
    # Dietary restrictions gate
    
    # Restriction details (conditional)
    ("Do you need **Gluten-Free** options?", "restrictions", "gluten-free", "yes_no", lambda: 'gluten-free' not in st.session_state.answers.get('restrictions', [])),
    ("Do you need **Dairy-Free** options?", "restrictions", "dairy-free", "yes_no", lambda: 'vegan' not in st.session_state.answers.get('diet', []) and 'lactose-free' not in st.session_state.answers.get('restrictions', [])),
    ("Are you looking for **Low-Carb** recipes?", "restrictions", "low-carb", "yes_no", lambda: st.session_state.answers.get('has_restrictions')),
    
    # Core questions - always ask
    ("What's your cooking experience?", "skill", "beginner", "skill", None),
    ("What's your budget per meal?", "budget", 20.0, "budget", None),
    ("How much time can you spend cooking?", "time", 30, "time", None),
    
    # Equipment gate
    ("Do you have **kitchen equipment**? (oven, stove, blender, etc.)", "has_equipment", True, "yes_no", None),
    
    # Equipment details (conditional)
    ("Do you have an **Oven**?", "equipment", "oven", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Stove/Pan**?", "equipment", "pan", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Microwave**?", "equipment", "microwave", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Blender**?", "equipment", "blender", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Food Processor**?", "equipment", "food processor", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have an **Air Fryer**?", "equipment", "air fryer", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Slow Cooker**?", "equipment", "slow cooker", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Grill**?", "equipment", "grill", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    ("Do you have a **Knife** (for chopping)?", "equipment", "knife", "yes_no", lambda: st.session_state.answers.get('has_equipment')),
    
    # Health goals gate
    ("Do you have specific **health or fitness goals**?", "has_health_goals", True, "yes_no", None),
    
    # Health goal details (conditional)
    ("Are you looking for **High-Protein** recipes?", "health_goals", "high-protein", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
    ("Are you looking for **Low-Calorie** recipes?", "health_goals", "low-calorie", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
    ("Is **Weight Loss** one of your goals?", "health_goals", "weight-loss", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
    ("Is **Muscle Gain** one of your goals?", "health_goals", "muscle-gain", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
    ("Is **Heart Health** important to you?", "health_goals", "heart-health", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
    ("Do you need to control **Blood Sugar**?", "health_goals", "blood-sugar-control", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
    ("Are you looking for an **Energy Boost**?", "health_goals", "energy-boost", "yes_no", lambda: st.session_state.answers.get('has_health_goals')),
]

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'answers' not in st.session_state:
    st.session_state.answers = {
        'has_allergies': [],
        'allergies': [],
        'has_special_diet': [],
        'diet': [],
        'has_restrictions': [],
        'restrictions': [],
        'skill': [],
        'budget': [],
        'time': [],
        'has_equipment': [],
        'equipment': [],
        'has_health_goals': [],
        'health_goals': []
    }

if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False

if 'show_confirmation' not in st.session_state:
    st.session_state.show_confirmation = False

if 'inference_complete' not in st.session_state:
    st.session_state.inference_complete = False


def answer_question(answer, custom_value=None):
    # Save answer and go to next question
    question_text, category, value, q_type, condition = QUESTIONS[st.session_state.current_question]
    
    if custom_value is not None:
        # For special questions (skill, budget, time)
        if answer:
            st.session_state.answers[category] = [custom_value]
    else:
        # For yes/no questions
        if answer:
            st.session_state.answers[category].append(value)
        # For gate questions, store boolean
        if category in ['has_allergies', 'has_special_diet', 'has_restrictions', 'has_equipment', 'has_health_goals']:
            st.session_state.answers[category] = answer
    
    # Find next question that should be asked
    st.session_state.current_question += 1
    while st.session_state.current_question < len(QUESTIONS):
        _, _, _, _, condition = QUESTIONS[st.session_state.current_question]
        # If no condition or condition is met, ask this question
        if condition is None or (callable(condition) and condition()):
            break
        # Skip this question
        st.session_state.current_question += 1
    
    # Check if quiz is complete
    if st.session_state.current_question >= len(QUESTIONS):
        st.session_state.quiz_complete = True
        st.session_state.show_confirmation = True


def reset_quiz():
    # Reset quiz state
    st.session_state.current_question = 0
    st.session_state.answers = {
        'has_allergies': [],
        'allergies': [],
        'has_special_diet': [],
        'diet': [],
        'has_restrictions': [],
        'restrictions': [],
        'skill': [],
        'budget': [],
        'time': [],
        'has_equipment': [],
        'equipment': [],
        'has_health_goals': [],
        'health_goals': []
    }
    st.session_state.quiz_complete = False
    st.session_state.show_confirmation = False
    st.session_state.inference_complete = False


def load_all_recipes():
    # Load recipes from YAML file
    recipes_file = Path(__file__).parent / 'data' / 'recipes.yaml'
    
    with open(recipes_file, 'r') as f:
        data = yaml.safe_load(f)
    
    recipes = []
    for recipe_data in data.get('recipes', []):
        # Parse ingredients
        ingredients = []
        for ing_data in recipe_data.get('ingredients', []):
            ingredient = Ingredient(
                name=ing_data['name'],
                quantity=ing_data.get('quantity', 0),
                unit=ing_data.get('unit', ''),
                allergens=ing_data.get('allergens', [])
            )
            ingredients.append(ingredient)
        
        # Parse nutritional info
        nutr_data = recipe_data.get('nutritional_info', {})
        nutritional_info = NutritionalInfo(
            calories=nutr_data.get('calories', 0),
            protein=nutr_data.get('protein', 0),
            carbohydrates=nutr_data.get('carbohydrates', 0),
            fat=nutr_data.get('fat', 0),
            fiber=nutr_data.get('fiber', 0),
            sodium=nutr_data.get('sodium', 0)
        )
        
        # Create recipe
        recipe = Recipe(
            name=recipe_data['name'],
            description=recipe_data.get('description', ''),
            ingredients=ingredients,
            equipment=recipe_data.get('equipment', []),
            cooking_time=str(recipe_data.get('cooking_time_minutes', 30)) + ' minutes',
            skill=recipe_data.get('skill_level', 'beginner').lower(),
            cost=recipe_data.get('cost', 10.0),
            nutritional_info=nutritional_info,
            cuisine=recipe_data.get('cuisine', 'Unknown'),
            instructions=recipe_data.get('instructions', []),
            diet=recipe_data.get('diet', 'omnivore').lower(),
            servings=recipe_data.get('servings', 1),
            tags=recipe_data.get('tags', [])
        )
        recipes.append(recipe)
    
    return recipes


def get_recommendation_reasons(recipe, user, working_memory):
    # Make a list of reasons for recommending a recipe
    reasons = []
    recipe_name_lower = recipe.name.lower().replace(' ', '_')
    
    # Check diet compatibility
    user_diet = st.session_state.answers.get('diet', [])
    if 'vegan' in user_diet:
        if recipe.diet == 'vegan':
            reasons.append("✅ **Vegan-friendly** - matches your diet preference")
    elif 'vegetarian' in user_diet:
        if recipe.diet in ['vegan', 'vegetarian']:
            reasons.append("✅ **Vegetarian-friendly** - matches your diet preference")
    elif 'pescatarian' in user_diet:
        if recipe.diet in ['vegan', 'vegetarian', 'pescatarian']:
            reasons.append("✅ **Pescatarian-friendly** - matches your diet preference")
    
    # Check dietary restrictions
    restrictions = st.session_state.answers.get('restrictions', [])
    if 'gluten-free' in restrictions:
        # Check if recipe has no gluten
        has_gluten = any('gluten' in ing.allergens or 'wheat' in ing.allergens for ing in recipe.ingredients)
        if not has_gluten:
            reasons.append("✅ **Gluten-free** - safe for your restriction")
    
    if 'dairy-free' in restrictions:
        # Check if recipe has no dairy
        has_dairy = any('dairy' in ing.allergens for ing in recipe.ingredients)
        if not has_dairy:
            reasons.append("✅ **Dairy-free** - safe for your restriction")
    
    if 'low-carb' in restrictions:
        if recipe.nutritional_info and recipe.nutritional_info.carbohydrates <= 30:
            reasons.append(f"✅ **Low-carb** - {recipe.nutritional_info.carbohydrates}g carbs per serving")
    
    # Check allergies (no allergic ingredients)
    user_allergies = st.session_state.answers.get('allergies', [])
    if user_allergies:
        recipe_allergens = set()
        for ing in recipe.ingredients:
            recipe_allergens.update(ing.allergens)
        
        has_conflict = any(allergy in recipe_allergens for allergy in user_allergies)
        if not has_conflict:
            reasons.append(f"✅ **Allergy-safe** - avoids your allergens ({', '.join(user_allergies)})")
    
    # Check skill level
    user_skill = st.session_state.answers.get('skill', ['beginner'])[0]
    if recipe.skill.lower() == user_skill or recipe.skill in ['beginner', 'easy']:
        reasons.append(f"✅ **Skill-appropriate** - matches your {user_skill} level")
    
    # Check budget
    user_budget = st.session_state.answers.get('budget', [20.0])[0]
    if recipe.cost <= user_budget:
        reasons.append(f"✅ **Within budget** - ${recipe.cost:.2f} ≤ ${user_budget:.2f}")
    
    # Check equipment
    user_equipment = set(st.session_state.answers.get('equipment', []))
    recipe_equipment = set([eq.lower() for eq in recipe.equipment])
    if user_equipment:
        # Check if user has necessary equipment
        compatible = True
        for req_eq in recipe_equipment:
            if req_eq not in user_equipment and req_eq not in ['bowl', 'spoon', 'knife']:  # basic items assumed
                compatible = False
                break
        if compatible and recipe_equipment:
            reasons.append(f"✅ **Equipment compatible** - you have the needed tools")
    
    # Check nutritional goals
    health_goals = st.session_state.answers.get('health_goals', [])
    if 'high-protein' in health_goals:
        if recipe.nutritional_info and recipe.nutritional_info.protein >= 20:
            reasons.append(f"✅ **High protein** - {recipe.nutritional_info.protein}g per serving")
    if 'low-calorie' in health_goals:
        if recipe.nutritional_info and recipe.nutritional_info.calories <= 400:
            reasons.append(f"✅ **Low calorie** - {recipe.nutritional_info.calories} kcal per serving")
    if 'weight-loss' in health_goals:
        if recipe.nutritional_info and recipe.nutritional_info.calories <= 350:
            reasons.append(f"✅ **Weight loss friendly** - {recipe.nutritional_info.calories} kcal per serving")
    if 'muscle-gain' in health_goals:
        if recipe.nutritional_info and recipe.nutritional_info.protein >= 25:
            reasons.append(f"✅ **Muscle building** - {recipe.nutritional_info.protein}g protein per serving")
    if 'heart-health' in health_goals:
        if recipe.nutritional_info and recipe.nutritional_info.fat <= 15:
            reasons.append(f"✅ **Heart-healthy** - {recipe.nutritional_info.fat}g fat per serving")
    
    # Check working memory for specific inference facts
    for fact in working_memory:
        # Recipe-specific suitability
        if f"recipe_suitable({recipe_name_lower})" in fact.lower():
            reasons.append("✅ **Inferred as suitable** - derived through forward-chaining")
            break
    
    # If no specific reasons found, provide general one
    if not reasons:
        reasons.append("✅ **Recommended by inference engine** - passed all constraint checks")
    
    return reasons


 # Show quiz questions one at a time
if not st.session_state.quiz_complete:
    # Figure out how many questions we've asked
    total_to_ask = sum(1 for i, (_, _, _, _, cond) in enumerate(QUESTIONS) 
                       if i <= st.session_state.current_question and 
                       (cond is None or (callable(cond) and cond())))
    
    # Show progress bar
    progress = st.session_state.current_question / len(QUESTIONS)
    st.progress(progress)
    st.caption(f"Question {total_to_ask} (skipped {st.session_state.current_question - total_to_ask + 1} irrelevant)")
    
    st.divider()
    
    # Ask the current question
    question_text, category, value, q_type, condition = QUESTIONS[st.session_state.current_question]
    st.subheader(question_text)
    st.write("")  # spacing
    
    # Skill level question
    if q_type == "skill":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👶 Beginner", key=f"skill_beginner", use_container_width=True):
                answer_question(True, "beginner")
                st.rerun()
        
        with col2:
            if st.button("👨‍🍳 Medium", key=f"skill_medium", use_container_width=True):
                answer_question(True, "medium")
                st.rerun()
        
        with col3:
            if st.button("⭐ Experienced", key=f"skill_experienced", use_container_width=True):
                answer_question(True, "experienced")
                st.rerun()
    
    # Budget question
    elif q_type == "budget":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💵 Under $10", key=f"budget_low", use_container_width=True):
                answer_question(True, 10.0)
                st.rerun()
        
        with col2:
            if st.button("💰 $10-30", key=f"budget_mid", use_container_width=True):
                answer_question(True, 20.0)
                st.rerun()
        
        with col3:
            if st.button("💎 $30+", key=f"budget_high", use_container_width=True):
                answer_question(True, 50.0)
                st.rerun()
    
    # Time question
    elif q_type == "time":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⚡ < 15 min", key=f"time_short", use_container_width=True):
                answer_question(True, 15)
                st.rerun()
        
        with col2:
            if st.button("🕐 15-45 min", key=f"time_medium", use_container_width=True):
                answer_question(True, 45)
                st.rerun()
        
        with col3:
            if st.button("🕰️ > 45 min", key=f"time_long", use_container_width=True):
                answer_question(True, 90)
                st.rerun()
    
    # Yes/No questions
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes", key=f"yes_{st.session_state.current_question}", use_container_width=True, type="primary"):
                answer_question(True)
                st.rerun()
        
        with col2:
            if st.button("❌ No", key=f"no_{st.session_state.current_question}", use_container_width=True, type="secondary"):
                answer_question(False)
                st.rerun()
    
    st.divider()
    
    # Reset quiz button
    if st.button("🔄 Reset Quiz", use_container_width=False):
        reset_quiz()
        st.rerun()


 # Show summary and confirm before inference
elif st.session_state.show_confirmation and not st.session_state.inference_complete:
    st.success("✅ Quiz Complete!")
    st.divider()
    
    st.subheader("📋 Your Preferences Summary")
    st.write("Please review your answers before we find your perfect recipes:")
    st.write("")
    
    # Show what the user picked
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚫 Dietary Restrictions")
        if st.session_state.answers.get('has_allergies'):
            if st.session_state.answers['allergies']:
                st.write("**Allergies:**", ", ".join(st.session_state.answers['allergies']))
            else:
                st.write("**Allergies:** None specified")
        else:
            st.write("**No food allergies**")
        
        if st.session_state.answers.get('has_special_diet'):
            if st.session_state.answers['diet']:
                diet_list = st.session_state.answers['diet']
                if 'vegan' in diet_list:
                    diet_display = "Vegan"
                elif 'vegetarian' in diet_list:
                    diet_display = "Vegetarian"
                elif 'pescatarian' in diet_list:
                    diet_display = "Pescatarian"
                else:
                    diet_display = "Omnivore"
                st.write("**Diet:**", diet_display)
            else:
                st.write("**Diet:** Omnivore")
        else:
            st.write("**No special diet requirements**")
        
        if st.session_state.answers.get('has_restrictions'):
            if st.session_state.answers.get('restrictions'):
                st.write("**Restrictions:**", ", ".join(st.session_state.answers['restrictions']))
            else:
                st.write("**No additional restrictions**")
        
        st.markdown("#### 👨‍🍳 Cooking Profile")
        skill_display = st.session_state.answers['skill'][0] if st.session_state.answers['skill'] else "beginner"
        st.write("**Skill Level:**", skill_display.title())
        
        time_display = st.session_state.answers['time'][0] if st.session_state.answers['time'] else 30
        st.write("**Max Cooking Time:**", f"{time_display} minutes")
    
    with col2:
        st.markdown("#### 💰 Budget & Equipment")
        budget_display = st.session_state.answers['budget'][0] if st.session_state.answers['budget'] else 20.0
        st.write("**Budget per meal:**", f"${budget_display:.0f}")
        
        if st.session_state.answers.get('has_equipment'):
            if st.session_state.answers['equipment']:
                st.write("**Equipment:**", ", ".join(st.session_state.answers['equipment']))
            else:
                st.write("**Equipment:** None specified")
        else:
            st.write("**No special equipment available**")
        
        st.markdown("#### 🎯 Health Goals")
        if st.session_state.answers.get('has_health_goals'):
            if st.session_state.answers['health_goals']:
                st.write(", ".join(st.session_state.answers['health_goals']))
            else:
                st.write("None specified")
        else:
            st.write("**No specific health goals**")
    
    st.divider()
    
    # Confirm or restart
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("✅ Yes, Find My Recipes!", use_container_width=True, type="primary"):
            st.session_state.inference_complete = True
            st.session_state.show_confirmation = False
            st.rerun()
    
    with col2:
        if st.button("🔄 Start Over", use_container_width=True, type="secondary"):
            reset_quiz()
            st.rerun()


 # Run inference and show results
elif st.session_state.inference_complete:
    st.success("🔍 Running Forward-Chaining Inference...")
    st.divider()
    
    # Make User object
    all_dietary_restrictions = st.session_state.answers['diet'] + st.session_state.answers.get('restrictions', [])
    
    user = User(
        name="User",
        allergies=st.session_state.answers['allergies'],
        dietary_restrictions=all_dietary_restrictions,
        available_equipment=st.session_state.answers['equipment'],
        skill_level=st.session_state.answers['skill'][0] if st.session_state.answers['skill'] else 'beginner',
        budget=st.session_state.answers['budget'][0] if st.session_state.answers['budget'] else 20.0,
        max_cooking_time=st.session_state.answers['time'][0] if st.session_state.answers['time'] else 60,
        health_goals=st.session_state.answers['health_goals']
    )
    
    # Load recipes
    all_recipes = load_all_recipes()
    
    # Run inference engine
    kb_path = Path(__file__).parent / 'inference' / 'knowledge_base.yaml'
    engine = InferenceEngine(str(kb_path))
    
    with st.spinner("🧠 Running inference engine..."):
        recommended = engine.forward_chain(user, user, all_recipes)
    
    # Show stats from inference
    st.info(f"**Inference Stats:** Derived {len(engine.working_memory)} facts through forward-chaining")
    
    if recommended:
        st.success(f"✅ Found {len(recommended)} recipe(s) matching your preferences!")
        st.divider()
        
        # Show each recommended recipe
        for i, recipe in enumerate(recommended, 1):
            with st.expander(f"📖 {i}. {recipe.name}", expanded=(i == 1)):
                # List reasons for recommendation
                reasons = get_recommendation_reasons(recipe, user, engine.working_memory)
                
                # Show reasons
                st.markdown("### 🎯 Why This Recipe?")
                for reason in reasons:
                    st.markdown(reason)
                
                st.markdown("---")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if recipe.description:
                        st.markdown(f"*{recipe.description}*")
                        st.write("")
                    
                    st.write(f"**🍽️ Cuisine:** {recipe.cuisine}")
                    st.write(f"**👨‍🍳 Skill Level:** {recipe.skill.title()}")
                    st.write(f"**⏱️ Cooking Time:** {recipe.cooking_time}")
                    st.write(f"**👥 Servings:** {recipe.servings}")
                    st.write(f"**💰 Cost:** ${recipe.cost:.2f}")
                    
                    st.markdown("---")
                    
                    # Show ingredients
                    if recipe.ingredients:
                        st.markdown("**🥕 Ingredients:**")
                        for ingredient in recipe.ingredients:
                            qty_unit = f"{ingredient.quantity} {ingredient.unit}" if ingredient.unit else str(ingredient.quantity)
                            allergen_note = f" ⚠️ *({', '.join(ingredient.allergens)})*" if ingredient.allergens else ""
                            st.write(f"- {qty_unit} {ingredient.name}{allergen_note}")
                    
                    st.markdown("---")
                    
                    # Show instructions
                    if recipe.instructions:
                        st.markdown("**📝 Instructions:**")
                        for idx, instruction in enumerate(recipe.instructions, 1):
                            st.write(f"{idx}. {instruction}")
                
                with col2:
                    # Show nutrition info
                    if recipe.nutritional_info:
                        st.markdown("**📊 Nutrition (per serving):**")
                        st.metric("Calories", f"{recipe.nutritional_info.calories} kcal")
                        st.write(f"🥩 Protein: {recipe.nutritional_info.protein}g")
                        st.write(f"🍞 Carbs: {recipe.nutritional_info.carbohydrates}g")
                        st.write(f"🧈 Fat: {recipe.nutritional_info.fat}g")
                        st.write(f"🌾 Fiber: {recipe.nutritional_info.fiber}g")
                    
                    # Show tags
                    if recipe.tags:
                        st.markdown("**🏷️ Tags:**")
                        st.write(", ".join(recipe.tags))
    else:
        st.warning("😕 No recipes match your criteria. Try adjusting your preferences!")
    
    st.divider()
    
    # Show inference facts
    with st.expander("🧠 View Inference Facts (Working Memory)", expanded=False):
        st.markdown("**These facts were derived through forward-chaining inference:**")
        st.write("")
        
        if engine.working_memory:
            for i, fact in enumerate(sorted(engine.working_memory), 1):
                st.write(f"{i}. `{fact}`")
        else:
            st.write("No facts derived")
        
        st.caption(f"Total facts derived: {len(engine.working_memory)}")
    
    st.divider()
    
    # Start new search button
    if st.button("🔄 Start New Search", use_container_width=True, type="primary"):
        reset_quiz()
        st.rerun()

st.divider()