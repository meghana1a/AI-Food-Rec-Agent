# AI Food Recommendation Agent 🍳 

An intelligent food recommendation system powered by DSPy and LLM that suggests recipes based on available ingredients, dietary preferences, and cuisine types.

## Features

- **Smart Recipe Suggestions**: Get 3-5 recipe recommendations based on your available ingredients
- **Dietary Accommodations**: Supports vegetarian, vegan, gluten-free, and other dietary restrictions
- **Cuisine Preferences**: Filter recommendations by cuisine type (Italian, Asian, Mexican, Mediterranean, etc.)
- **Meal Type Selection**: Get suggestions for breakfast, lunch, dinner, or snacks
- **Missing Ingredients**: Identifies ingredients that could enhance your dishes
- **Cooking Tips**: Provides helpful cooking tips for recommended dishes
- **Recipe Database**: Includes fallback recipe matching from a built-in database

## Prerequisites

- Python 3.8+
- API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Food-Rec-Agent.git
cd AI-Food-Rec-Agent
```

2. Install required dependencies:
```bash
pip install dspy-ai groq
```

3. Set up your Groq API key:
```bash
# Linux/Mac
export GROQ_API_KEY="your_api_key_here"

# Windows (Command Prompt)
set GROQ_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GROQ_API_KEY="your_api_key_here"
```

## Usage

### Running the Application

```bash
python food_recommendation_agent.py
```

You'll be presented with three options:
1. **Interactive Mode** - Enter your own ingredients and preferences
2. **Demo Mode** - See example recommendations with preset ingredients
3. **Exit**


## Code Structure

```
food_recommendation_agent.py
├── FoodRecommendation       # DSPy signature defining input/output fields
├── FoodRecommenderAgent     # Main agent class using Chain of Thought
├── RecipeDatabase           # Static recipe database for fallback suggestions
├── interactive_food_recommender()  # Interactive user interface
└── demo_recommendations()   # Demo scenarios
```

## Troubleshooting

### API Key Issues
If you see "Error: GROQ_API_KEY environment variable is required":
1. Ensure you've set the environment variable correctly
2. Verify your API key is valid
3. Check you have an active internet connection

### Model Errors
If the model fails to respond:
1. Check your API key has sufficient credits
2. Verify the model name is correct
3. Ensure you're not hitting rate limits

## License

This project is part of AI POCs (Proof of Concepts) for educational and demonstration purposes.

## Acknowledgments

- Built with [DSPy](https://github.com/stanfordnlp/dspy) framework
- Powered by [Groq](https://groq.com/) API
- Uses Llama 3.1 70B language model
- README written by Claude

