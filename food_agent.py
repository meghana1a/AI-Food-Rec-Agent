import dspy
from typing import List, Dict
import json
import os

groq_api_key = os.getenv("GROQ_API_KEY")

lm = dspy.LM(
    model="add model",  
    api_key=groq_api_key,
    temperature=0.7,
    max_tokens=2048
)
dspy.settings.configure(lm=lm)


class FoodRecommendation(dspy.Signature):
    ingredients = dspy.InputField(desc="List of available ingredients")
    dietary_restrictions = dspy.InputField(desc="Any dietary restrictions (vegetarian, vegan, gluten-free, etc.)", default="none")
    cuisine_preference = dspy.InputField(desc="Preferred cuisine type (Italian, Asian, Mexican, etc.)", default="any")
    meal_type = dspy.InputField(desc="Type of meal (breakfast, lunch, dinner, snack)", default="any")
    
    recommendations = dspy.OutputField(desc="List of 3-5 recommended dishes with brief recipes")
    missing_ingredients = dspy.OutputField(desc="Common ingredients that could enhance the dishes")
    cooking_tips = dspy.OutputField(desc="General cooking tips for the recommended dishes")


class FoodRecommenderAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.recommend = dspy.ChainOfThought(FoodRecommendation)
        
    def forward(self, ingredients, dietary_restrictions="none", cuisine_preference="any", meal_type="any"):
        result = self.recommend(
            ingredients=ingredients,
            dietary_restrictions=dietary_restrictions,
            cuisine_preference=cuisine_preference,
            meal_type=meal_type
        )
        return result


class RecipeDatabase:
    @staticmethod
    def get_sample_recipes():
        return [
            {
                "name": "Pasta Carbonara",
                "ingredients": ["pasta", "eggs", "bacon", "parmesan cheese", "black pepper"],
                "cuisine": "Italian",
                "meal_type": "dinner"
            },
            {
                "name": "Vegetable Stir-fry",
                "ingredients": ["rice", "mixed vegetables", "soy sauce", "garlic", "ginger"],
                "cuisine": "Asian",
                "meal_type": "lunch",
                "dietary": "vegetarian"
            },
            {
                "name": "Greek Salad",
                "ingredients": ["tomatoes", "cucumber", "feta cheese", "olives", "olive oil"],
                "cuisine": "Mediterranean",
                "meal_type": "lunch",
                "dietary": "vegetarian"
            },
            {
                "name": "Scrambled Eggs with Toast",
                "ingredients": ["eggs", "bread", "butter", "milk", "salt"],
                "cuisine": "American",
                "meal_type": "breakfast",
                "dietary": "vegetarian"
            },
            {
                "name": "Chicken Tacos",
                "ingredients": ["chicken", "tortillas", "lettuce", "tomatoes", "cheese", "salsa"],
                "cuisine": "Mexican",
                "meal_type": "dinner"
            }
        ]
    
    @staticmethod
    def find_matching_recipes(ingredients_list, cuisine=None, dietary=None):
        recipes = RecipeDatabase.get_sample_recipes()
        matching = []
        
        ingredients_set = set(i.lower().strip() for i in ingredients_list)
        
        for recipe in recipes:
            recipe_ingredients = set(i.lower() for i in recipe["ingredients"])
            
            # Check if we have at least 60% of the ingredients
            overlap = ingredients_set.intersection(recipe_ingredients)
            if len(overlap) >= len(recipe_ingredients) * 0.6:
                if cuisine and cuisine.lower() != "any":
                    if recipe.get("cuisine", "").lower() != cuisine.lower():
                        continue
                if dietary and dietary.lower() != "none":
                    if recipe.get("dietary", "").lower() != dietary.lower():
                        continue
                
                matching.append({
                    "recipe": recipe,
                    "matching_ingredients": list(overlap),
                    "missing_ingredients": list(recipe_ingredients - ingredients_set)
                })
        
        return matching


def interactive_food_recommender():
    print("\n=== AI Food Recommendation Agent ===\n")
    recommender = FoodRecommenderAgent()
    
    while True:
        print("\n--- New Recommendation Request ---")
        
        # ingredients
        ingredients_input = input("\nEnter your available ingredients (comma-separated): ")
        if ingredients_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the Food Recommendation Agent!")
            break
        
        # dietary restrictions
        dietary = input("Any dietary restrictions? (vegetarian/vegan/gluten-free/none): ").strip() or "none"
        
        # cuisine preference
        cuisine = input("Preferred cuisine? (Italian/Asian/Mexican/Mediterranean/any): ").strip() or "any"
        
        # meal type
        meal = input("Meal type? (breakfast/lunch/dinner/snack/any): ").strip() or "any"
        
        print("\n Analyzing ingredients and generating recommendations...\n")
        
        # DSPy agent
        try:
            result = recommender(
                ingredients=ingredients_input,
                dietary_restrictions=dietary,
                cuisine_preference=cuisine,
                meal_type=meal
            )
            
            print("RECOMMENDED DISHES:")
            print("-" * 50)
            print(result.recommendations)
            
            print("\nINGREDIENTS YOU MIGHT WANT TO ADD:")
            print("-" * 50)
            print(result.missing_ingredients)
            
            print("\nCOOKING TIPS:")
            print("-" * 50)
            print(result.cooking_tips)
            
            ingredients_list = [i.strip() for i in ingredients_input.split(',')]
            db_matches = RecipeDatabase.find_matching_recipes(
                ingredients_list, 
                cuisine=cuisine,
                dietary=dietary
            )
            
            if db_matches:
                print("\n FROM RECIPE DATABASE:")
                print("-" * 50)
                for match in db_matches[:3]:
                    recipe = match["recipe"]
                    print(f"\n• {recipe['name']} ({recipe['cuisine']} - {recipe['meal_type']})")
                    print(f"  You have: {', '.join(match['matching_ingredients'])}")
                    if match['missing_ingredients']:
                        print(f"  Missing: {', '.join(match['missing_ingredients'])}")
            
        except Exception as e:
            print(f"\n Error generating recommendations: {e}")
            print("Please make sure your API key is set correctly.")
        
        continue_prompt = input("\n\nWould you like another recommendation? (yes/no): ")
        if continue_prompt.lower() not in ['yes', 'y']:
            print("\nThank you for using the Food Recommendation Agent!")
            break


def demo_recommendations():
    print("\n=== Food Recommendation Agent Demo ===\n")
    
    recommender = FoodRecommenderAgent()
    
    demos = [
        {
            "ingredients": "chicken, rice, onions, garlic, tomatoes, olive oil",
            "dietary": "none",
            "cuisine": "Mediterranean",
            "meal": "dinner"
        },
        {
            "ingredients": "eggs, bread, cheese, spinach, mushrooms",
            "dietary": "vegetarian",
            "cuisine": "any",
            "meal": "breakfast"
        },
        {
            "ingredients": "pasta, tomatoes, basil, garlic, olive oil, mozzarella",
            "dietary": "vegetarian",
            "cuisine": "Italian",
            "meal": "lunch"
        },
        {
            "ingredients": "tofu, soy sauce, rice, broccoli, carrots, ginger",
            "dietary": "vegan",
            "cuisine": "Asian",
            "meal": "dinner"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{'='*60}")
        print(f"DEMO {i}: {demo['cuisine']} {demo['meal']}")
        print(f"{'='*60}")
        print(f"Ingredients: {demo['ingredients']}")
        print(f"Dietary: {demo['dietary']}")
        
        try:
            result = recommender(
                ingredients=demo['ingredients'],
                dietary_restrictions=demo['dietary'],
                cuisine_preference=demo['cuisine'],
                meal_type=demo['meal']
            )
            
            print("\n Recommendations:")
            print(result.recommendations)
            
            print("\n Additional ingredients to consider:")
            print(result.missing_ingredients)
            
            print("\n Tips:")
            print(result.cooking_tips)
            
        except Exception as e:
            print(f"\n Demo failed: {e}")
            print("Note: You need a Groq API key for the demos to work.")
            print("Get a free key at: https://console.groq.com/keys")


if __name__ == "__main__":
    print("\n Welcome to the AI Food Recommendation Agent! 🍳")
    print("\nThis agent helps you discover what you can cook with your available ingredients.")
    print("\nChoose an option:")
    print("1. Interactive mode - Enter your own ingredients")
    print("2. Demo mode - See example recommendations")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1/2/3): ")
    
    if choice == "1":
        interactive_food_recommender()
    elif choice == "2":
        demo_recommendations()
    else:
        print("\nGoodbye! Happy cooking!")