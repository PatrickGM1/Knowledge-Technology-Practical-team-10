"""Utility functions for the recipe recommender system"""

from typing import Dict, List
from models import User, Diet, DietRestriction, Skill, CookingTime, CookingMethod, Macros


def preferences_to_user(preferences: Dict[str, List]) -> User:
    """Convert quiz preferences dictionary to User object
    
    Args:
        preferences: Dictionary containing user's quiz responses with keys like
                    'diet', 'diet_restrictions', 'skill', 'cooking_time', etc.
    
    Returns:
        User object with preferences converted to appropriate attributes
    """
    # Extract dietary restrictions
    dietary_restrictions = []
    allergies = []
    
    for restriction in preferences.get('diet_restrictions', []):
        if restriction == DietRestriction.LACTOSE_INTOLERANT:
            allergies.append('dairy')
            dietary_restrictions.append('lactose-free')
        elif restriction == DietRestriction.GLUTEN_INTOLERANT:
            allergies.append('gluten')
            dietary_restrictions.append('gluten-free')
        elif restriction == DietRestriction.NUTS_ALLERGIES:
            allergies.append('nuts')
        elif restriction == DietRestriction.DIABETES:
            dietary_restrictions.append('low-sugar')
    
    # Extract diet type
    for diet in preferences.get('diet', []):
        if diet == Diet.VEGAN:
            dietary_restrictions.append('vegan')
        elif diet == Diet.VEGETARIAN:
            dietary_restrictions.append('vegetarian')
        elif diet == Diet.PESCATARIAN:
            dietary_restrictions.append('pescatarian')
    
    # Extract skill level
    skill_level = 'beginner'
    if preferences.get('skill'):
        skill = preferences['skill'][0]
        if skill == Skill.EASY:
            skill_level = 'beginner'
        elif skill == Skill.MEDIUM:
            skill_level = 'intermediate'
        elif skill == Skill.EXPERIENCED:
            skill_level = 'advanced'
    
    # Extract cooking methods to equipment
    available_equipment = []
    for method in preferences.get('cooking_methods', []):
        if method == CookingMethod.PAN:
            available_equipment.extend(['pan', 'stove'])
        elif method == CookingMethod.OVEN:
            available_equipment.append('oven')
        elif method == CookingMethod.GRILL:
            available_equipment.append('grill')
    
    # Extract time constraint
    max_time = None
    if preferences.get('cooking_time'):
        time = preferences['cooking_time'][0]
        if time == CookingTime.LESS_THAN_15:
            max_time = 15
        elif time == CookingTime.BETWEEN_15_45:
            max_time = 45
        elif time == CookingTime.MORE_THAN_45:
            max_time = 120
    
    # Extract health goals from macros
    health_goals = []
    for macro in preferences.get('macros', []):
        if macro == Macros.HIGH_PROTEIN:
            health_goals.append('high-protein')
        elif macro == Macros.LOW_FATS:
            health_goals.append('low-fat')
        elif macro == Macros.LOW_CARBS:
            health_goals.append('low-carb')
        elif macro == Macros.LOW_SUGARS:
            health_goals.append('low-sugar')
    
    return User(
        name="User",
        dietary_restrictions=list(set(dietary_restrictions)),
        allergies=list(set(allergies)),
        skill_level=skill_level,
        available_equipment=list(set(available_equipment)),
        max_cooking_time=max_time,
        health_goals=health_goals
    )
