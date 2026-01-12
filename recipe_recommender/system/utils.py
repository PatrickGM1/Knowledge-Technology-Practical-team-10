"""Utility functions for the recipe recommender system"""

from typing import Dict, List
from models import (
    User, Diet, DietRestriction, Skill, CookingTime, CookingMethod, Macros, Budget,
    Allergy, BudgetConstraint, CookingSkill, TimeConstraint, 
    DietaryPreference, HealthGoal, Kitchen
)


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
    
    # Create domain objects
    allergies_list = [Allergy(allergen_name=a, severity='moderate') for a in allergies]
    
    skill_obj = CookingSkill(level=skill_level, years_experience=0)
    
    time_constraint_obj = TimeConstraint(
        available_minutes=max_time if max_time else 120,
        includes_prep=True,
        flexibility=False
    ) if max_time else None
    
    # Create dietary preference
    diet_type = 'omnivore'
    for diet in preferences.get('diet', []):
        if diet == Diet.VEGAN:
            diet_type = 'vegan'
            break
        elif diet == Diet.VEGETARIAN:
            diet_type = 'vegetarian'
            break
        elif diet == Diet.PESCATARIAN:
            diet_type = 'pescatarian'
            break
    
    dietary_pref = DietaryPreference(
        type=diet_type,
        restrictions=dietary_restrictions,
        preferred_cuisines=[]
    )
    
    # Create health goals
    health_goals_list = [HealthGoal(goal_type=goal, priority='medium') for goal in health_goals]
    
    # Create budget constraint
    budget_pref = 'moderate'
    if preferences.get('budget'):
        budget_enum = preferences['budget'][0]
        if budget_enum == Budget.BUDGET:
            budget_pref = 'budget'
        elif budget_enum == Budget.PREMIUM:
            budget_pref = 'premium'
    
    budget_obj = BudgetConstraint(preferred_range=budget_pref, flexibility='flexible')
    
    # Create kitchen
    kitchen_obj = Kitchen(
        available_equipment=list(set(available_equipment)),
        available_utensils=[],
        space_size='medium'
    )
    
    return User(
        name="User",
        dietary_restrictions=list(set(dietary_restrictions)),
        allergies=list(set(allergies)),
        skill_level=skill_level,
        available_equipment=list(set(available_equipment)),
        max_cooking_time=max_time,
        health_goals=health_goals,
        # Domain objects
        allergies_list=allergies_list,
        budget=budget_obj,
        skill=skill_obj,
        time_constraint=time_constraint_obj,
        dietary_preference=dietary_pref,
        health_goals_list=health_goals_list,
        kitchen=kitchen_obj
    )

