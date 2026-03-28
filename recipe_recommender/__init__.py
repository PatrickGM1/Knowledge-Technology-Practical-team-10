"""
Recipe Recommendation System with Forward-Chaining Inference

Project Structure:
- domainClasses/    : Real-world domain concepts (Recipe, Ingredient, etc.)
- constraints/      : User preferences and limitations (User, Allergy, Kitchen, etc.)
- inference/        : AI reasoning system (InferenceEngine, Rule, KnowledgeBase)
- data/            : Reference data (cooking methods, meal types)
"""

__version__ = '2.0.0'
__author__ = 'Team 10'

# Import main components for easy access
from .domainClasses import Recipe, Ingredient, Equipment, NutritionalInfo, Cuisine
from .constraints import User, Kitchen, Allergy, DietaryPreference, CookingSkill
from .inference import InferenceEngine, KnowledgeBase, Rule
from .data import COOKING_METHODS, MEAL_TYPES

__all__ = [
    # Domain Classes
    'Recipe',
    'Ingredient',
    'Equipment',
    'NutritionalInfo',
    'Cuisine',
    
    # User Constraints
    'User',
    'Kitchen',
    'Allergy',
    'DietaryPreference',
    'CookingSkill',
    
    # Inference System
    'InferenceEngine',
    'KnowledgeBase',
    'Rule',
    
    # Reference Data
    'COOKING_METHODS',
    'MEAL_TYPES',
]
