# Knowledge Technology Practical - Team 10

This is our recipe recommender project for the Knowledge Technology practical.

In short, it is a rule-based system where:
- the UI is built in Streamlit
- recipes are stored in YAML
- recommendation logic is done with a forward-chaining inference engine

## What It Does

The app asks the user a set of questions (allergies, diet, budget, time, equipment, goals, etc.) and then recommends recipes that fit those constraints.

It does not just filter by tags. It applies rules, derives facts, and then shows recommendations with reasons.

## Stack

- Python
- Streamlit
- PyYAML

Dependencies are in [recipe_recommender/requirements.txt](recipe_recommender/requirements.txt).

## Main Files

- [recipe_recommender/main.py](recipe_recommender/main.py): Streamlit app and quiz flow
- [recipe_recommender/inference/inference_engine.py](recipe_recommender/inference/inference_engine.py): forward-chaining logic
- [recipe_recommender/inference/knowledge_base.yaml](recipe_recommender/inference/knowledge_base.yaml): rule definitions
- [recipe_recommender/data/recipes.yaml](recipe_recommender/data/recipes.yaml): recipe data
- [recipe_recommender/domainClasses](recipe_recommender/domainClasses): recipe/domain models
- [recipe_recommender/constraints](recipe_recommender/constraints): user and constraint models

## Run Locally

From the repo root:

```bash
python -m pip install -r recipe_recommender/requirements.txt
streamlit run recipe_recommender/main.py
```

Then open the local URL printed by Streamlit in your terminal.

## How The Reasoning Works

The engine does forward chaining in a loop:
1. Load initial facts from the user profile and recipes.
2. Check rules from the knowledge base.
3. Fire matching rules and update facts (for example suitability, score, exclusions, substitutions).
4. Repeat until nothing new is derived (or max iterations is reached).
5. Return the final recommended recipes.


