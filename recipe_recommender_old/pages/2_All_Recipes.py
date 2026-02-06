import streamlit as st
from data.sample_recipes import get_all_recipes

st.set_page_config(
    page_title="All Recipes",
    layout="wide"
)

st.title("📚 All Available Recipes")
st.write("Browse through all recipes in our database")
st.divider()

# Get all recipes
all_recipes = get_all_recipes()

# Add filters in sidebar
st.sidebar.header("Filter Recipes")

# Diet filter
diet_options = sorted(list(set([recipe.diet.value for recipe in all_recipes])))
selected_diets = st.sidebar.multiselect("Diet Type", diet_options)

# Skill level filter
skill_options = sorted(list(set([recipe.skill.value for recipe in all_recipes])))
selected_skills = st.sidebar.multiselect("Skill Level", skill_options)

# Cooking time filter
time_options = sorted(list(set([recipe.cooking_time.value for recipe in all_recipes])))
selected_times = st.sidebar.multiselect("Cooking Time", time_options)

# Budget filter
budget_options = sorted(list(set([recipe.budget.value for recipe in all_recipes])))
selected_budgets = st.sidebar.multiselect("Budget", budget_options)

# Meal type filter
meal_options = sorted(list(set([recipe.meal.value for recipe in all_recipes])))
selected_meals = st.sidebar.multiselect("Meal Type", meal_options)

# Cooking method filter
cooking_method_options = sorted(list(set([method.value for recipe in all_recipes for method in recipe.cooking_methods])))
selected_methods = st.sidebar.multiselect("Cooking Method", cooking_method_options)

# Cuisine filter
cuisine_options = sorted(list(set([recipe.cuisine for recipe in all_recipes if recipe.cuisine])))
selected_cuisines = st.sidebar.multiselect("Cuisine", cuisine_options)

# Dietary restrictions filter
restriction_options = sorted(list(set([r.value for recipe in all_recipes for r in recipe.diet_restrictions if r.value != "none"])))
selected_restrictions = st.sidebar.multiselect("Suitable For (Dietary Restrictions)", restriction_options)

# Macros/Nutrition focus filter
macro_options = sorted(list(set([m.value for recipe in all_recipes for m in recipe.macros])))
selected_macros = st.sidebar.multiselect("Nutrition Focus", macro_options)

# Servings filter
st.sidebar.subheader("Servings Range")
min_servings = st.sidebar.number_input("Minimum Servings", min_value=1, max_value=10, value=1)
max_servings = st.sidebar.number_input("Maximum Servings", min_value=1, max_value=10, value=10)

# Cost filter
st.sidebar.subheader("Cost Range (€)")
costs = [recipe.cost for recipe in all_recipes if recipe.cost]
if costs:
    min_cost = min(costs)
    max_cost = max(costs)
    cost_range = st.sidebar.slider(
        "Cost per serving",
        min_value=float(min_cost),
        max_value=float(max_cost),
        value=(float(min_cost), float(max_cost)),
        step=0.5
    )
else:
    cost_range = (0, 100)

# Calories filter
st.sidebar.subheader("Nutrition Ranges")
calories_list = [recipe.nutritional_info.calories for recipe in all_recipes if recipe.nutritional_info and recipe.nutritional_info.calories]
if calories_list:
    min_cal = min(calories_list)
    max_cal = max(calories_list)
    calorie_range = st.sidebar.slider(
        "Calories",
        min_value=int(min_cal),
        max_value=int(max_cal),
        value=(int(min_cal), int(max_cal)),
        step=10
    )
else:
    calorie_range = (0, 1000)

# Protein filter
protein_list = [recipe.nutritional_info.protein for recipe in all_recipes if recipe.nutritional_info and recipe.nutritional_info.protein]
if protein_list:
    min_prot = min(protein_list)
    max_prot = max(protein_list)
    protein_range = st.sidebar.slider(
        "Protein (g)",
        min_value=int(min_prot),
        max_value=int(max_prot),
        value=(int(min_prot), int(max_prot)),
        step=1
    )
else:
    protein_range = (0, 100)

# Apply filters (show all if no filters selected)
filtered_recipes = [
    recipe for recipe in all_recipes
    if (not selected_diets or recipe.diet.value in selected_diets)
    and (not selected_skills or recipe.skill.value in selected_skills)
    and (not selected_times or recipe.cooking_time.value in selected_times)
    and (not selected_budgets or recipe.budget.value in selected_budgets)
    and (not selected_meals or recipe.meal.value in selected_meals)
    and (not selected_methods or any(method.value in selected_methods for method in recipe.cooking_methods))
    and (not selected_cuisines or recipe.cuisine in selected_cuisines)
    and (not selected_restrictions or any(r.value in selected_restrictions for r in recipe.diet_restrictions))
    and (not selected_macros or any(m.value in selected_macros for m in recipe.macros))
    and (recipe.servings >= min_servings and recipe.servings <= max_servings)
    and (not recipe.cost or (recipe.cost >= cost_range[0] and recipe.cost <= cost_range[1]))
    and (not recipe.nutritional_info or not recipe.nutritional_info.calories or 
         (recipe.nutritional_info.calories >= calorie_range[0] and recipe.nutritional_info.calories <= calorie_range[1]))
    and (not recipe.nutritional_info or not recipe.nutritional_info.protein or 
         (recipe.nutritional_info.protein >= protein_range[0] and recipe.nutritional_info.protein <= protein_range[1]))
]

# Display summary
st.info(f"Showing {len(filtered_recipes)} of {len(all_recipes)} recipes")

# Display recipes
for recipe in filtered_recipes:
    with st.expander(f"📖 {recipe.name}", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if recipe.description:
                st.markdown(f"**{recipe.description}**")
            
            st.write(f"🍽️ **Cuisine:** {recipe.cuisine if recipe.cuisine else 'N/A'}")
            if recipe.prep_time:
                st.write(f"⏱️ **Prep Time:** {recipe.prep_time} min")
            st.write(f"🕐 **Cooking Time:** {recipe.cooking_time.value}")
            st.write(f"👨‍🍳 **Skill Level:** {recipe.skill.value}")
            st.write(f"🍴 **Servings:** {recipe.servings}")
            st.write(f"🥗 **Diet:** {recipe.diet.value}")
            st.write(f"💰 **Budget:** {recipe.budget.value}")
            st.write(f"🍳 **Meal Type:** {recipe.meal.value}")
            
            # Cooking methods
            methods = [m.value for m in recipe.cooking_methods]
            st.write(f"🔥 **Cooking Methods:** {', '.join(methods)}")
            
            # Dietary restrictions
            restrictions = [r.value for r in recipe.diet_restrictions if r.value != "none"]
            if restrictions:
                st.write(f"✅ **Suitable for:** {', '.join(restrictions)}")
            
            # Macros
            if recipe.macros:
                macros = [m.value for m in recipe.macros]
                st.write(f"💪 **Nutrition Focus:** {', '.join(macros)}")
            
            st.divider()
            
            if recipe.ingredients:
                st.markdown("**Ingredients:**")
                for ingredient in recipe.ingredients:
                    optional = " (optional)" if ingredient.is_optional else ""
                    prep = f", {ingredient.preparation}" if ingredient.preparation else ""
                    st.write(f"- {ingredient.quantity} {ingredient.unit} {ingredient.name}{prep}{optional}")
                    
                    # Show substitutes if available
                    if ingredient.substitutes:
                        subs = ", ".join(ingredient.substitutes.keys())
                        st.caption(f"   *Can substitute with: {subs}*")
            
            if recipe.equipment:
                st.markdown("**Equipment:**")
                equip_list = [eq.name for eq in recipe.equipment]
                st.write(", ".join(equip_list))
            
            if recipe.instructions:
                st.markdown("**Instructions:**")
                for i, instruction in enumerate(recipe.instructions, 1):
                    st.write(f"{i}. {instruction}")
        
        with col2:
            if recipe.nutritional_info:
                st.markdown("**Nutrition (per serving):**")
                st.write(f"🔥 {recipe.nutritional_info.calories} cal")
                st.write(f"🥩 {recipe.nutritional_info.protein}g protein")
                st.write(f"🍞 {recipe.nutritional_info.carbohydrates}g carbs")
                st.write(f"🧈 {recipe.nutritional_info.fat}g fat")
                st.write(f"🌾 {recipe.nutritional_info.fiber}g fiber")
                st.write(f"🧂 {recipe.nutritional_info.sodium}mg sodium")
                if recipe.nutritional_info.sugar:
                    st.write(f"🍯 {recipe.nutritional_info.sugar}g sugar")
            
            if recipe.cost:
                st.divider()
                st.metric("Cost per serving", f"€{recipe.cost:.2f}")

st.divider()
st.caption(f"Total recipes in database: {len(all_recipes)}")
