# Knowledge Technology Practical – Team 10

This repository contains the work for the **Knowledge Technology Practical**, completed by **Team 10**.  
It includes project files, code, and documentation related to the course.

## Project Idea
**Recipe Recommendation System**  
A knowledge-based system that recommends recipes using an inference engine with modular rules, hierarchical domain model, and declarative knowledge base.

## Team Members
- **Ana Maria Izbas** – S5575974 – *Analyst / Documentation Lead*  
- **George Radu Tutui** – S5515610 – *Knowledge Engineer (Chef Interviewer)*  
- **Mihai Patrick Gheba** – S5560535 – *Developer*

These are our **main roles**, but we will **collaborate and support each other** throughout all stages of the project.

---

## Documentation

**Note**: The documentation files referenced below (QUICK_START.md, KNOWLEDGE_BASE_README.md, etc.) do not currently exist in the repository. The main documentation is in this README.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

## Overview

The Recipe Recommender is an intelligent knowledge-based system that helps users find recipes matching their preferences using a sophisticated inference engine. The system features:

**Hierarchical Domain Model** (13 classes)
- **User**: Profiles with dietary restrictions, allergies, skill level, equipment, time constraints, health goals
- **Recipe**: Recipes with ingredients, equipment, cooking methods (6 types: Pan, Oven, Grill, Marinated, Bowl, Blender), nutritional info
- **Ingredient**: Ingredients with category, nutritional properties, allergen information, substitutes
- **Equipment**: Kitchen equipment with type, alternatives, availability
- **DetailedCookingMethod**: Cooking methods with temperature, duration, substitutions
- **NutritionalInfo**: Nutritional data with health goal evaluation (high protein, low calorie, high fiber)
- **Allergy**: Allergen types with tracking
- **HealthGoal**: Health objectives (weight loss, muscle building, heart health, diabetes management, general wellness)
- **DietaryPreference**: Dietary options (vegan, vegetarian, pescatarian, gluten-free, lactose-free, nut-free)
- **CookingSkill**: Skill levels (beginner, intermediate, experienced)
- **TimeConstraint**: Time availability constraints
- **BudgetConstraint**: Budget categories (budget, moderate, premium)
- **Kitchen**: Kitchen setup with available equipment

**Inference Engine**
- **51 modular rules** in YAML knowledge base (declarative, separate from code)
- **Filtering Rules**: Exclude recipes based on allergies (13 specific allergen rules including dairy, milk, cheese, butter, cream, yogurt), diet, time, skill, equipment, cuisine
- **Scoring Rules**: Rank recipes by cuisine match, health goals, speed, difficulty, budget, nutrition
- **Substitution Rules**: Suggest alternatives for dairy, meat, gluten, cooking methods, equipment
- **Priority-based execution**: Rules evaluated in order (0-100 priority)
- **Declarative conditions**: Operators include ==, !=, >, <, in, contains, method_call
- **Context-aware reasoning**: Rules operate on User and Recipe domain objects

**Smart Recommendations**
- Dietary preferences (Vegan, Vegetarian, Pescatarian, Omnivore)
- Dietary restrictions & allergies (Lactose, Gluten, Nuts, etc.)
- Cooking time constraints
- Skill level matching (Beginner, Intermediate, Advanced)
- Cuisine preferences (Italian, American, etc.)
- Health goals (High Protein, Low Carb, etc.)
- Equipment availability
- Ingredient substitutions

---

## Quick Start

```bash
# Navigate to project
cd recipe_recommender

# Install dependencies (if needed)
pip install streamlit pyyaml

# Run the app
streamlit run main.py --server.port=8505
```

Open browser to: **http://localhost:8505**

---

## Features

### Interactive Quiz Interface
- **Comprehensive allergen tracking**: 9 allergen questions (dairy, milk, cheese, butter, cream, yogurt, nuts, gluten, eggs)
- **Health goals selection**: 5 health goal options (weight loss, muscle building, heart health, diabetes management, general wellness)
- **Equipment availability**: 8 equipment questions (pan, oven, grill, blender, bowl, special equipment)
- **Dietary preferences**: 7 options (vegan, vegetarian, pescatarian, gluten-free, lactose-free, nut-free, none)
- **Step-by-step questionnaire**: Guided questions to capture user preferences
- **Progress tracking**: Visual progress bar showing quiz completion
- **Smart question flow**: Questions adapt based on previous answers
- **Multiple question types**: Yes/No, multi-choice buttons, and option selectors
- **Custom styling**: Color-coded buttons for intuitive user experience

### Recipe Filtering & Scoring
- **Filtering rules**: Comprehensive rules to exclude recipes based on 13+ allergens, diet, time, skill, equipment
- **Scoring rules**: Rank recipes by relevance (cuisine match, health goals, speed, etc.)
- **Substitution suggestions**: Ingredient/method alternatives (dairy, meat, gluten, equipment)
- **Priority-based execution**: Rules processed by priority (highest first)
- **Reason explanations**: Every filter/score includes human-readable explanation

### User Experience
- **Clean, modern UI**: Built with Streamlit for responsive web interface
- **Detailed results**: Each recipe shows score, ranking reasons, and substitution suggestions
- **Real-time recommendations**: Inference engine processes rules instantly
- **Reset functionality**: Easy quiz restart for trying different preferences
- **Mobile-friendly**: Responsive design works on various screen sizes

---

## System Architecture

### Domain Model (13 Classes)
The system implements a hierarchical object-oriented domain model:

- **User**: User profile with dietary restrictions, allergies, preferences, skill level, equipment, time constraints, health goals
- **Recipe**: Recipe with ingredients, equipment, cooking methods (Pan, Oven, Grill, Marinated, Bowl, Blender), nutritional info, skill level, time, budget
- **Ingredient**: Ingredient with category, nutritional properties, allergen info, substitutes
- **Equipment**: Kitchen equipment with type, alternatives, availability
- **DetailedCookingMethod**: Cooking methods with temperature, duration, substitutions
- **NutritionalInfo**: Nutritional data with health goal evaluation methods
- **Allergy**: Allergen type definitions and tracking
- **HealthGoal**: Health objectives (weight loss, muscle building, heart health, diabetes management, general wellness)
- **DietaryPreference**: Dietary options (vegan, vegetarian, pescatarian, gluten-free, lactose-free, nut-free)
- **CookingSkill**: Skill levels with recipe complexity matching
- **TimeConstraint**: Time availability constraints for cooking
- **BudgetConstraint**: Budget categories for recipe cost filtering
- **Kitchen**: Kitchen setup with available equipment and capabilities

### Inference Engine Architecture
The system uses a knowledge-based inference engine with:

1. **Knowledge Base (51 Rules in YAML)**:
   - Filtering Rules (allergies with 13 specific rules for dairy/milk/cheese/butter/cream/yogurt/nuts/gluten/eggs/soy/fish/shellfish/sesame, diet, time, skill, equipment, cuisine)
   - Scoring Rules (cuisine match, health goals, quick recipes, beginner-friendly, budget, low-calorie, high-fiber)
   - Substitution Rules (dairy alternatives, meat alternatives, gluten-free, cooking methods, equipment)

2. **Rule Structure**:
   - Priority-based execution (0-100)
   - Declarative conditions with operators (==, !=, >, <, in, contains, method_call)
   - Actions: filter (exclude recipes), score (rank recipes), substitute (suggest alternatives)

3. **Inference Process**:
   - Load rules from `knowledge_base.yaml`
   - Evaluate conditions against User and Recipe objects
   - Execute actions based on rule priority
   - Return filtered, scored recipes with substitution suggestions

4. **Recipe Database**:
   - 20 diverse recipes covering Italian, French, British, American, Mexican, Romanian, Mediterranean, Middle Eastern, and Asian cuisines
   - 6 cooking methods: Pan, Oven, Grill, Marinated, Bowl, Blender
   - Full dietary spectrum: Vegan, Vegetarian, Pescatarian, Omnivore
   - Complete nutritional data and ingredient substitutions
   - Includes Chef Sorin's handwritten recipes and team-contributed recipes

### System Workflow
```
User Quiz → User Object → Inference Engine → Knowledge Base
                             ↓
            Filter Rules → Score Rules → Substitution Rules
                             ↓
            Ranked Recommendations + Alternatives
```

### Filtering Logic
The recommendation engine uses declarative rule-based filtering with priority execution:
1. **Allergy filtering** (Priority 100): Exclude recipes with allergens
2. **Diet matching** (Priority 90): Recipe diet must match user preference
3. **Restriction enforcement** (Priority 85): Exclude disliked ingredients
4. **Time constraints** (Priority 80): Recipe cooking time within limits
5. **Skill alignment** (Priority 75): Recipe complexity matches user skill
6. **Equipment availability** (Priority 70): Required equipment available
7. **Health goals** (Priority 65): Recipe matches nutritional targets
8. **Cuisine preferences** (Priority 60): Preferred cuisines prioritized

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/PatrickGM1/Knowledge-Technology-Practical-team-10.git
   cd Knowledge-Technology-Practical-team-10/recipe_recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will launch automatically

---

## Usage

### Starting the Quiz
1. Launch the application using `streamlit run main.py`
2. The interactive quiz will begin automatically
3. Read each question carefully and select your preference

### Answering Questions

**Yes/No Questions** (Diet, Restrictions, Cooking Methods, Macros):
- Green "Yes" button: Select this preference
- Red "No" button: Skip this preference

**Time Questions**:
- "Less": <15 minutes cooking time
- "Yes": 15-45 minutes cooking time
- "More": >45 minutes cooking time

**Skill Level**:
- "Beginner": Easy recipes
- "Intermediate": Medium difficulty recipes
- "Experienced": Advanced recipes

**Budget**:
- "Student Life": Lowest cost recipes
- "Budget Friendly": Moderate cost recipes
- "Gourmet": Premium ingredient recipes

**Meal Type**:
- Choose from: Breakfast, Lunch, Dinner, Snack, Dessert

### Viewing Results
- After completing all questions, view your preference summary
- See all selected criteria organized by category
- View recommended recipes with scores, reasons, and substitution suggestions
- Use "Start Over" to reset and try different preferences

### Resetting
- Click "Reset Quiz" at any time to start fresh
- All answers will be cleared and quiz returns to question 1

---

## Project Structure

```
recipe_recommender/
├── main.py                          # Streamlit app with comprehensive quiz interface
├── requirements.txt                 # Python dependencies (streamlit, pyyaml, pytest)
├── knowledge_base.yaml              # 51 declarative rules for inference engine
├── testGUI.py                       # Alternative GUI implementation
├── HOW_TO_ADD_RECIPES.md           # Guide for adding new recipes
├── models/
│   ├── __init__.py                 # Model exports
│   ├── user.py                     # User class with preferences/constraints
│   ├── recipe.py                   # Recipe class + enums (Diet, Skill, CookingMethod, etc.)
│   ├── ingredient.py               # Ingredient class
│   ├── equipment.py                # Equipment class
│   ├── cooking_method.py           # DetailedCookingMethod class
│   ├── nutritional_info.py         # NutritionalInfo class
│   ├── allergy.py                  # Allergy enum
│   ├── budget_constraint.py        # BudgetConstraint class
│   ├── health_goal.py              # HealthGoal enum
│   ├── time_constraint.py          # TimeConstraint class
│   ├── cooking_skill.py            # CookingSkill class
│   ├── dietary_preference.py       # DietaryPreference enum
│   └── kitchen.py                  # Kitchen class
├── data/
│   ├── __init__.py
│   └── sample_recipes.py           # 20 sample recipes with full data
├── system/
│   ├── __init__.py                 # System exports
│   ├── inference_engine.py         # Rule evaluation engine (Rule, InferenceEngine)
│   └── utils.py                    # Utility functions (preferences_to_user)
├── pages/
│   └── 1_Team_Info.py              # Team information page
└── tests/
    ├── __init__.py
    └── test_gui_inference.py       # Comprehensive test suite (68 tests)
```

### Key Files

- **`main.py`**: Streamlit interface with comprehensive quiz flow, allergen tracking, health goals, and result display
- **`knowledge_base.yaml`**: 51 rules (filtering with 13+ allergen rules, scoring, substitution)
- **`system/inference_engine.py`**: Core engine with Rule and InferenceEngine classes
- **`models/recipe.py`**: Recipe class + enums (Diet, DietRestriction, CookingTime, Skill, CookingMethod with 6 values, Budget, Meal, Macros)
- **`models/cooking_method.py`**: DetailedCookingMethod class with properties, alternatives, skill matching
- **`data/sample_recipes.py`**: 20 diverse recipes covering 9 cuisines (French, British, Italian, American, Mexican, Mediterranean, Middle Eastern, Asian, Romanian)
- **`pages/2_All_Recipes.py`**: Recipe browsing page with 13 filter options
- **`tests/test_gui_inference.py`**: 59 comprehensive tests ensuring system reliability

---

## Testing

The project includes a comprehensive test suite with **68 tests** covering:

- **Inference Engine Tests**: Knowledge base loading, rule evaluation, filtering logic
- **Recipe Tests**: All 20 recipes validated for proper structure and attributes
- **New Recipe Tests**: 15 dedicated tests for newly added recipes (Beef Wellington, Potato Puree, Asparagus Soup, Couscous, Hummus)
- **Cooking Method Tests**: Validation of all 6 cooking methods (Pan, Oven, Grill, Marinated, Bowl, Blender)
- **Filtering Tests**: Allergy filtering, dietary restrictions, time constraints, skill matching
- **Integration Tests**: End-to-end testing of quiz → inference → recommendations

### Running Tests

```bash
cd recipe_recommender
pytest tests/ -v
```

All 68 tests pass successfully, ensuring system reliability and correctness.

---

## Technologies Used

- **[Python 3.13](https://www.python.org/)**: Core programming language
- **[Streamlit](https://streamlit.io/)**: Web application framework for interactive UI
- **[PyYAML](https://pyyaml.org/)**: YAML parser for knowledge base loading
- **[Pytest](https://pytest.org/)**: Testing framework with 68 comprehensive tests
- **Object-Oriented Design**: Extended domain model with 13 classes
- **Knowledge Representation**: Declarative rules in YAML format (51 rules)
- **Inference Engine**: Priority-based rule evaluation with context-aware reasoning

### Dependencies
```
streamlit>=1.28.0
pyyaml>=6.0
pytest>=9.0.0
```

### Running the Application
```bash
# Development mode
streamlit run main.py --server.port=8501

# Production mode
streamlit run main.py --server.port=8501 --server.headless=true
```

### Testing the Inference Engine
```bash
# Run comprehensive test suite (68 tests)
cd recipe_recommender
pytest tests/ -v

# Quick validation test
python -c "
from system import InferenceEngine
from data.sample_recipes import get_all_recipes
from models import User

# Test knowledge base loading
engine = InferenceEngine('knowledge_base.yaml')
print(f'Loaded {len(engine.rules)} rules')

# Test recipe database
recipes = get_all_recipes()
print(f'Available recipes: {len(recipes)}')

# Test with vegan user
user = User(name='Test', dietary_restrictions=['vegan'])
results = engine.apply_rules(user, recipes)
print(f'Vegan-friendly recipes: {len(results)}')
"
```

---

