# Knowledge Technology Practical – Team 10

This repository contains the work for the **Knowledge Technology Practical**, completed by **Team 10**.  
It includes project files, code, and documentation related to the course.

## Project Idea
**Recipe Recommendation System**  
A system that recommends recipes based on user preferences, available ingredients, and expert chef knowledge.

## Team Members
- **Ana Maria Izbas** – S5575974 – *Analyst / Documentation Lead*  
- **George Radu Tutui** – S5515610 – *Knowledge Engineer (Chef Interviewer)*  
- **Mihai Patrick Gheba** – S5560535 – *Developer*

These are our **main roles**, but we will **collaborate and support each other** throughout all stages of the project.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

## Overview

The Recipe Recommender is an intelligent system that helps users find recipes matching their dietary preferences, restrictions, cooking skills, and available time. The system uses a knowledge-based approach to filter and recommend recipes based on multiple criteria including:

- Dietary preferences (Vegan, Vegetarian, Pescatarian, Omnivore)
- Dietary restrictions (Lactose intolerance, Gluten intolerance, Nut allergies, Diabetes)
- Cooking time availability
- Skill level (Beginner, Intermediate, Experienced)
- Cooking methods (Pan, Oven, Grill)
- Budget constraints (Student Life, Budget Friendly, Gourmet)
- Meal type (Breakfast, Lunch, Dinner, Snack, Dessert)
- Nutritional goals (High Protein, Low Fat, Low Carb, Low Sugar)

---

## Features

### Interactive Quiz Interface
- **Step-by-step questionnaire**: 20 guided questions to capture user preferences
- **Progress tracking**: Visual progress bar showing quiz completion
- **Smart question flow**: Questions adapt based on previous answers
- **Multiple question types**: Yes/No, multi-choice buttons, and option selectors
- **Custom styling**: Color-coded buttons for intuitive user experience

### Recipe Filtering
- **Multi-criteria filtering**: Recipes matched against all user preferences
- **Flexible matching**: Accommodates partial matches for cooking methods and macros
- **Dietary restriction enforcement**: Ensures recipes are safe for user allergies/restrictions
- **Preference summary**: Clear display of all selected preferences

### User Experience
- **Clean, modern UI**: Built with Streamlit for responsive web interface
- **Reset functionality**: Easy quiz restart for trying different preferences
- **Real-time updates**: Immediate feedback as users progress through questions
- **Mobile-friendly**: Responsive design works on various screen sizes

---

## System Architecture- [Development](#development)


### Data Models
The system uses enum-based data models for type safety and clarity:

- **Recipe**: Core recipe model with all attributes
- **Diet**: Vegan, Vegetarian, Pescatarian, Omnivore
- **DietRestriction**: Lactose intolerant, Gluten intolerant, Nut allergies, Diabetes, None
- **CookingTime**: <15 min, 15-45 min, >45 min
- **Skill**: Easy, Medium, Experienced
- **CookingMethod**: Pan, Oven, Grill
- **Budget**: Student Life, Budget Friendly, Gourmet
- **Meal**: Breakfast, Lunch, Dinner, Snack, Dessert
- **Macros**: High Protein, Low Fat, Low Carb, Low Sugar

### Filtering Logic
The recommendation engine uses rule-based filtering:
1. **Diet matching**: Recipe diet must match user preference
2. **Restriction enforcement**: All user restrictions must be accommodated
3. **Time constraints**: Recipe cooking time must match availability
4. **Skill alignment**: Recipe difficulty must match user skill level
5. **Method availability**: Recipe uses at least one available cooking method
6. **Budget compliance**: Recipe cost aligns with user budget
7. **Meal timing**: Recipe type matches desired meal
8. **Nutritional goals**: Recipe has at least one matching macro preference

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
- Use "Start Over" to reset and try different preferences

### Resetting
- Click "Reset Quiz" at any time to start fresh
- All answers will be cleared and quiz returns to question 1

---

## Project Structure

```
recipe_recommender/
├── main.py                 # Main Streamlit application with quiz interface
├── requirements.txt        # Python dependencies
├── models/
│   ├── __init__.py        # Model exports
│   └── recipe.py          # Recipe and enum data models
├── data/
│   └──__init__.py
│ 
├── pages/
│   └── 1_Team_Info.py     # Team information page
└── system/
    └── __init__.py        # System utilities
```

### Key Files

- **`main.py`**: Contains the complete quiz interface with all 20 questions, button styling, and result display
- **`models/recipe.py`**: Defines all data models using Python enums for type safety
- **`data/sample_recipes.py`**: Contains sample recipes and the `filter_recipes()` function
- **`pages/1_Team_Info.py`**: Supplementary page with team member information

---

## Technologies Used

- **[Python 3.x](https://www.python.org/)**: Core programming language
- **[Streamlit](https://streamlit.io/)**: Web application framework for ML/data science
- **[Python Enums](https://docs.python.org/3/library/enum.html)**: Type-safe enumeration for recipe attributes
- **HTML/CSS**: Custom styling for buttons and UI elements

### Dependencies
```
streamlit>=1.28.0
```

### Running in Development
```bash
streamlit run main.py 
```

---
