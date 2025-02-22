import json
import streamlit as st
import spacy
import random

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load recipes from JSON file
with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

# Randomized greetings and farewells
greetings = [
    "Ciao bella! 😊", "Salve, amico mio! 🍕", "Buongiorno! 🇮🇹", 
    "Benvenuto alla cucina di Noona! 🍝", "Ehilà! Pronto per cucinare? 🍷"
]
farewells = [
    "Buon appetito! 😋", "Alla prossima, chef! 🍽️", "Arrivederci, e buon pasto! 🇮🇹",
    "Mangia bene, vivi meglio! 🍕", "Ci vediamo presto! 🍷"
]

def find_best_recipe(user_ingredients):
    best_match = None
    best_match_count = 0

    for recipe, details in recipes.items():
        recipe_ingredients = set(details["ingredients"])
        matched_ingredients = recipe_ingredients.intersection(user_ingredients)
        match_count = len(matched_ingredients)

        if match_count > best_match_count:
            best_match = recipe
            best_match_count = match_count

    return best_match

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>NoonaBot 🇮🇹 - Your Italian Recipe Assistant</h1>", unsafe_allow_html=True)

# Bigger and styled input label
st.markdown("<h3>🍅🥖 What ingredients do you have? 🍝🥕</h3>", unsafe_allow_html=True)

# User input
user_input = st.text_input("Enter ingredients (e.g., spaghetti, basil, cheese)")

if user_input:
    user_ingredients = set([token.text.lower() for token in nlp(user_input) if token.is_alpha])

    best_recipe = find_best_recipe(user_ingredients)

    if best_recipe:
        st.markdown(f"<h2 style='text-align: center; font-weight: bold;'>{best_recipe}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px;'>{random.choice(greetings)} How about making <strong>{best_recipe}</strong>? 🍽️</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px;'><strong>🥦 Ingredients:</strong> {', '.join(recipes[best_recipe]['ingredients'])}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px;'><strong>📖 Instructions:</strong> {recipes[best_recipe]['instructions']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px;'><em>{random.choice(farewells)}</em></p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size: 18px;'>{random.choice(greetings)} Mi dispiace, I couldn't find a recipe with those ingredients. Try listing different ones! 🍽️</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px;'><em>{random.choice(farewells)}</em></p>", unsafe_allow_html=True)
