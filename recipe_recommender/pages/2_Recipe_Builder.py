import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from models import (
    Recipe, Diet, DietRestriction, CookingTime, 
    Skill, CookingMethod, Budget, Meal, Macros
)


st.set_page_config(page_title="Recipe Preferences", layout="wide")

st.title("🔍 Find Your Perfect Recipe")
st.write("Answer the questions one at a time to find recipes that match your preferences!")
st.divider()

QUESTIONS = [
    ("Are you Vegan?", "diet", Diet.VEGAN, "single"),
    ("Are you Vegetarian?", "diet", Diet.VEGETARIAN, "single"),
    ("Are you Pescatarian?", "diet", Diet.PESCATARIAN, "single"),
    
    ("Are you Lactose Intolerant?", "restrictions", DietRestriction.LACTOSE_INTOLERANT, "multiple"),
    ("Are you Gluten Intolerant?", "restrictions", DietRestriction.GLUTEN_INTOLERANT, "multiple"),
    ("Do you have Nut Allergies?", "restrictions", DietRestriction.NUTS_ALLERGIES, "multiple"),
    ("Do you have Diabetes?", "restrictions", DietRestriction.DIABETES, "multiple"),
    
    ("Do you have 15 to 45 minutes to cook?", "cooking_time", CookingTime.BETWEEN_15_45, "time"),
    
    ("What's your cooking skill level?", "skill", Skill.MEDIUM, "skill"),
    
    ("Do you want to use a Pan?", "cooking_methods", CookingMethod.PAN, "multiple"),
    ("Do you want to use an Oven?", "cooking_methods", CookingMethod.OVEN, "multiple"),
    ("Do you want to use a Grill?", "cooking_methods", CookingMethod.GRILL, "multiple"),
    
    ("What's your budget?", "budget", Budget.BUDGET_FRIENDLY, "budget"),
    
    ("What meal are you looking for?", "meal", Meal.LUNCH, "meal"),
    
    ("Do you want High Protein recipes?", "macros", Macros.HIGH_PROTEIN, "multiple"),
    ("Do you want Low Fat recipes?", "macros", Macros.LOW_FATS, "multiple"),
    ("Do you want Low Carb recipes?", "macros", Macros.LOW_CARBS, "multiple"),
    ("Do you want Low Sugar recipes?", "macros", Macros.LOW_SUGARS, "multiple"),
]

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    
if 'answers' not in st.session_state:
    st.session_state.answers = {
        'diet': [],
        'restrictions': [],
        'cooking_time': [],
        'skill': [],
        'cooking_methods': [],
        'budget': [],
        'meal': [],
        'macros': []
    }

if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False


def answer_question(answer, custom_value=None):
    """Process user's answer and advance to next question"""
def answer_question(answer, custom_value=None):
    """Process user's answer and advance to next question"""
    question_text, category, value, q_type = QUESTIONS[st.session_state.current_question]
    
    if custom_value is not None:
        if answer:
            st.session_state.answers[category].append(custom_value)
    else:
        if answer:
            st.session_state.answers[category].append(value)
    
    st.session_state.current_question += 1
    
    if q_type == "single" and answer:
        while (st.session_state.current_question < len(QUESTIONS) and 
               QUESTIONS[st.session_state.current_question][1] == category):
            st.session_state.current_question += 1
    
    if st.session_state.current_question < len(QUESTIONS):
        prev_category = category
        next_category = QUESTIONS[st.session_state.current_question][1]
        
        if prev_category == "diet" and next_category != "diet":
            if not st.session_state.answers["diet"]:
                st.session_state.answers["diet"].append(Diet.OMNIVORE)
        
        if prev_category == "restrictions" and next_category != "restrictions":
            if not st.session_state.answers["restrictions"]:
                st.session_state.answers["restrictions"].append(DietRestriction.NONE)
    
    if st.session_state.current_question >= len(QUESTIONS):
        if not st.session_state.answers["diet"]:
            st.session_state.answers["diet"].append(Diet.OMNIVORE)
        if not st.session_state.answers["restrictions"]:
            st.session_state.answers["restrictions"].append(DietRestriction.NONE)
        
        st.session_state.quiz_complete = True

def reset_quiz():
    """Clear all answers and restart from beginning"""
    st.session_state.current_question = 0
    st.session_state.answers = {
        'diet': [],
        'restrictions': [],
        'cooking_time': [],
        'skill': [],
        'cooking_methods': [],
        'budget': [],
        'meal': [],
        'macros': []
    }
    st.session_state.quiz_complete = False

if not st.session_state.quiz_complete:
    progress = st.session_state.current_question / len(QUESTIONS)
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS)}")
    
    st.divider()
    
    question_text, category, value, q_type = QUESTIONS[st.session_state.current_question]
    st.subheader(question_text)
    
    if q_type == "time":
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
            if st.button("Less", key="time_less", use_container_width=True, type="secondary"):
                answer_question(True, CookingTime.LESS_THAN_15)
                st.rerun()
        
        with col2:
            if st.button("Yes", key="time_yes", use_container_width=True, type="primary"):
                answer_question(True, CookingTime.BETWEEN_15_45)
                st.rerun()
        
        with col3:
            if st.button("More", key="time_more", use_container_width=True, type="secondary"):
                answer_question(True, CookingTime.MORE_THAN_45)
                st.rerun()
    
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
            if st.button("Beginner", key="skill_easy", use_container_width=True, type="secondary"):
                answer_question(True, Skill.EASY)
                st.rerun()
        
        with col2:
            if st.button("Intermediate", key="skill_medium", use_container_width=True, type="primary"):
                answer_question(True, Skill.MEDIUM)
                st.rerun()
        
        with col3:
            if st.button("Experienced", key="skill_exp", use_container_width=True, type="tertiary"):
                answer_question(True, Skill.EXPERIENCED)
                st.rerun()
    
    elif q_type == "budget":
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
            if st.button("Student Life", key="budget_student", use_container_width=True, type="secondary"):
                answer_question(True, Budget.STUDENT_LIFE)
                st.rerun()
        
        with col2:
            if st.button("Budget Friendly", key="budget_friendly", use_container_width=True, type="primary"):
                answer_question(True, Budget.BUDGET_FRIENDLY)
                st.rerun()
        
        with col3:
            if st.button("Gourmet", key="budget_gourmet", use_container_width=True, type="tertiary"):
                answer_question(True, Budget.GOURMET)
                st.rerun()
    
    elif q_type == "meal":
        st.markdown("""
            <style>
                div.stButton > button[kind="primary"] {
                    background-color: transparent;
                    color: #007bff;
                    border: 2px solid #007bff;
                }
                div.stButton > button[kind="primary"]:hover {
                    background-color: #007bff;
                    color: white;
                    border: 2px solid #007bff;
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
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("Breakfast", key="meal_breakfast", use_container_width=True, type="secondary"):
                answer_question(True, Meal.BREAKFAST)
                st.rerun()
        
        with col2:
            if st.button("Lunch", key="meal_lunch", use_container_width=True, type="secondary"):
                answer_question(True, Meal.LUNCH)
                st.rerun()
        
        with col3:
            if st.button("Dinner", key="meal_dinner", use_container_width=True, type="secondary"):
                answer_question(True, Meal.DINNER)
                st.rerun()
        
        with col4:
            if st.button("Snack", key="meal_snack", use_container_width=True, type="secondary"):
                answer_question(True, Meal.SNACK)
                st.rerun()
        
        with col5:
            if st.button("Dessert", key="meal_dessert", use_container_width=True, type="secondary"):
                answer_question(True, Meal.DESSERT)
                st.rerun()
    
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
            if st.button("Yes", key="yes_btn", use_container_width=True, type="primary"):
                answer_question(True)
                st.rerun()
        
        with col2:
            if st.button("No", key="no_btn", use_container_width=True, type="secondary"):
                answer_question(False)
                st.rerun()
    
    st.divider()
    
    if st.button("🔄 Reset Quiz", key="reset_btn", use_container_width=False):
        reset_quiz()
        st.rerun()

else:
    st.success("✅ All questions answered!")
    
    st.subheader("Your Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.answers['diet']:
            st.write(f"**Diet:** {', '.join([d.value.title() for d in st.session_state.answers['diet']])}")
        else:
            st.write("**Diet:** None selected")
            
        if st.session_state.answers['cooking_time']:
            st.write(f"**Cooking Time:** {', '.join([t.value.title() for t in st.session_state.answers['cooking_time']])}")
        else:
            st.write("**Cooking Time:** None selected")
            
        if st.session_state.answers['skill']:
            st.write(f"**Skill Level:** {', '.join([s.value.title() for s in st.session_state.answers['skill']])}")
        else:
            st.write("**Skill Level:** None selected")
            
        if st.session_state.answers['budget']:
            st.write(f"**Budget:** {', '.join([b.value.title() for b in st.session_state.answers['budget']])}")
        else:
            st.write("**Budget:** None selected")
    
    with col2:
        if st.session_state.answers['meal']:
            st.write(f"**Meal Type:** {', '.join([m.value.title() for m in st.session_state.answers['meal']])}")
        else:
            st.write("**Meal Type:** None selected")
            
        if st.session_state.answers['restrictions']:
            st.write(f"**Dietary Restrictions:** {', '.join([r.value.title() for r in st.session_state.answers['restrictions']])}")
        else:
            st.write("**Dietary Restrictions:** None selected")
            
        if st.session_state.answers['cooking_methods']:
            st.write(f"**Cooking Methods:** {', '.join([m.value.title() for m in st.session_state.answers['cooking_methods']])}")
        else:
            st.write("**Cooking Methods:** None selected")
            
        if st.session_state.answers['macros']:
            st.write(f"**Nutritional Goals:** {', '.join([m.value.title() for m in st.session_state.answers['macros']])}")
        else:
            st.write("**Nutritional Goals:** None selected")
    
    st.divider()
    
    st.session_state.preferences = st.session_state.answers
    
    st.info("💡 Once recipes are added to the system, they will be filtered based on your preferences!")
    
    if st.button("🔄 Start Over", use_container_width=True):
        reset_quiz()
        st.rerun()

