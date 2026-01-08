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

## 📚 Documentation

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

**🏗️ Hierarchical Domain Model** (6 classes)
- **User**: Profiles with dietary restrictions, allergies, skill level, equipment, time constraints, health goals
- **Recipe**: Recipes with ingredients, equipment, cooking methods, nutritional info
- **Ingredient**: Ingredients with category, nutritional properties, allergen information
- **Equipment**: Kitchen equipment with type, alternatives, availability
- **DetailedCookingMethod**: Cooking methods with temperature, duration, substitutions
- **NutritionalInfo**: Nutritional data with health goal evaluation (high protein, low calorie, high fiber)

**🧠 Inference Engine**
- **25 modular rules** in YAML knowledge base (declarative, separate from code)
- **11 Filtering Rules**: Exclude recipes based on allergies, diet, time, skill, equipment, cuisine
- **7 Scoring Rules**: Rank recipes by cuisine match, health goals, speed, difficulty, budget, nutrition
- **7 Substitution Rules**: Suggest alternatives for dairy, meat, gluten, cooking methods, equipment
- **Priority-based execution**: Rules evaluated in order (0-100 priority)
- **Declarative conditions**: Operators include ==, !=, >, <, in, contains, method_call
- **Context-aware reasoning**: Rules operate on User and Recipe domain objects

**🎯 Smart Recommendations**
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

### 🎨 Interactive Quiz Interface
- **Step-by-step questionnaire**: Guided questions to capture user preferences
### 🎨 Interactive Quiz Interface
- **Step-by-step questionnaire**: Guided questions to capture user preferences
- **Progress tracking**: Visual progress bar showing quiz completion
- **Smart question flow**: Questions adapt based on previous answers
- **Multiple question types**: Yes/No, multi-choice buttons, and option selectors
- **Custom styling**: Color-coded buttons for intuitive user experience

### Recipe Filtering & Scoringules to rank recipes by relevance (cuisine match, health goals, speed, etc.)
- **Substitution suggestions**: 7 rules for ingredient/method alternatives (dairy, meat, gluten, equipment)
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

### Domain Model (6 Classes)
The system implements a hierarchical object-oriented domain model:

- **User**: User profile with dietary restrictions, allergies, preferences, skill level, equipment, time constraints, health goals
- **Recipe**: Recipe with ingredients, equipment, cooking methods, nutritional info, skill level, time, budget
- **Ingredient**: Ingredient with category, nutritional properties, allergen info
- **Equipment**: Kitchen equipment with type, alternatives, availability
- **DetailedCookingMethod**: Cooking methods with temperature, duration, substitutions
- **NutritionalInfo**: Nutritional data with health goal evaluation methods

### Inference Engine Architecture
The system uses a knowledge-based inference engine with:

1. **Knowledge Base (25 Rules in YAML)**:
   - 11 Filtering Rules (allergies, diet, time, skill, equipment, cuisine)
   - 7 Scoring Rules (cuisine match, health goals, quick recipes, beginner-friendly, budget, low-calorie, high-fiber)
   - 7 Substitution Rules (dairy alternatives, meat alternatives, gluten-free, cooking methods, equipment)

2. **Rule Structure**:
   - Priority-based execution (0-100)
   - Declarative conditions with operators (==, !=, >, <, in, contains, method_call)
   - Actions: filter (exclude recipes), score (rank recipes), substitute (suggest alternatives)

3. **Inference Process**:
   - Load rules from `knowledge_base.yaml`
   - Evaluate conditions against User and Recipe objects
   - Execute actions based on rule priority
   - Return filtered, scored recipes with substitution suggestions

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
├── main.py                          # Streamlit app with quiz interface
├── requirements.txt                 # Python dependencies (streamlit, pyyaml)
├── knowledge_base.yaml              # 25 declarative rules for inference engine
├── models/
│   ├── __init__.py                 # Model exports
│   ├── user.py                     # User class with preferences/constraints
│   ├── recipe.py                   # Recipe class + enums (Diet, Skill, etc.)
│   ├── ingredient.py               # Ingredient class
│   ├── equipment.py                # Equipment class
│   ├── cooking_method.py           # CookingMethod class
│   └── nutritional_info.py         # NutritionalInfo class
├── data/
│   ├── __init__.py
│   └── sample_recipes.py           # 5 sample recipes with full data
├── system/
│   ├── __init__.py                 # System exports
│   ├── inference_engine.py         # Rule evaluation engine (Rule, InferenceEngine)
│   └── utils.py                    # Utility functions (preferences_to_user)
└── pages/
    └── 1_Team_Info.py              # Team information page
```

### Key Files

- **`main.py`**: Streamlit interface with quiz flow and result display
- **`knowledge_base.yaml`**: 25 rules (11 filtering, 7 scoring, 7 substitution)
- **`system/inference_engine.py`**: Core engine with Rule and InferenceEngine classes
- **`models/recipe.py`**: Recipe class + 8 enums (Diet, DietRestriction, CookingTime, Skill, CookingMethod enum, Budget, Meal, Macros)
- **`models/cooking_method.py`**: CookingMethod class with properties, alternatives, skill matching
- **`data/sample_recipes.py`**: 5 sample recipes with full details

---

## Technologies Used

- **[Python 3.13](https://www.python.org/)**: Core programming language
- **[Streamlit](https://streamlit.io/)**: Web application framework for interactive UI
- **[PyYAML](https://pyyaml.org/)**: YAML parser for knowledge base loading
- **Object-Oriented Design**: 6-class hierarchical domain model
- **Knowledge Representation**: Declarative rules in YAML format
- **Inference Engine**: Priority-based rule evaluation with context-aware reasoning

### Dependencies
```
streamlit>=1.28.0
pyyaml>=6.0
```

### Running the Application
```bash
# Development mode
streamlit run main.py --server.port=8505

# Production mode
streamlit run main.py --server.port=8505 --server.headless=true
```

### Testing the Inference Engine
```bash
# Run test script to verify all components
cd recipe_recommender
python -c "
from system import InferenceEngine
from data.sample_recipes import get_all_recipes
from models import User

# Test knowledge base loading
engine = InferenceEngine('knowledge_base.yaml')
print(f'Loaded {len(engine.rules)} rules')

# Test recipe filtering
recipes = get_all_recipes()
print(f'Available recipes: {len(recipes)}')

# Test with vegan user
user = User(name='Test', dietary_restrictions=['vegan'])
results = engine.apply_rules(user, recipes)
print(f'Filtered recipes: {len(results)}')
"
```

---

### Dependencies
```
streamlit>=1.28.0
```

### Running in Development
```bash
streamlit run main.py 
```

---
