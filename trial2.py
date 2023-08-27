
import openai
import json
from main import get_recipe
from main import get_nutrients
from main import get_meals_and_compare_nutrients
from main import get_meal_based_on_restriction



def get_answer(question):
    messages = [{'role': 'user', 'content': question}]
    functions = [
        {
            "name": "get_recipe",
            "description": """Get ingredients about meals
            """,
            "parameters":{
                "type":"object",
                "properties":{
                    "nutrients":{
                        "type":"object",
                        "description":"denotes the quantities in grams of different nutrients in the meal"
                    },
                    "recipe":{
                        "type":"object",
                        "description":"ingredients used to make the meal"
                    },
                    "name":{
                        "type":"string",
                        "description":"unique name of the meal"
                    }
                }
            }
        },
        {
            "name":"get_nutrients",
            "description":"""Get all nutrient related information about meals""",
            "parameters":{
                "type": "object",
                "properties": {
                    "nutrients": {
                        "type": "object",
                        "description": "denotes the quantities in grams of different nutrients in the meal"
                    },
                    "recipe": {
                        "type": "object",
                        "description": "ingredients used to make the meal"
                    },
                    "name": {
                        "type": "string",
                        "description": "unique name of the meal"
                    }
                }
            }
        },
        {
            "name": "get_and_compare_nutrients_between_2_meals",
            "description": """Get all nutrient related information about 2 meals and compare specified nutrient""",
            "parameters": {
                "type": "object",
                "properties": {
                    "nutrients": {
                        "type": "object",
                        "description": "denotes the quantities in grams of different nutrients in the meal"
                    },
                    "recipe": {
                        "type": "object",
                        "description": "ingredients used to make the meal"
                    },
                    "name1": {
                        "type": "string",
                        "description": "unique name of the meal1"
                    },
                    "name2":{
                        "type":"string",
                        "description":"unique name of the meal2"
                    },
                    "nameofnutrient":{
                        "type":"string",
                        "description":"name of nutrient to compare"
                    },
                }
            },
            "required":["name1","name2","nameofnutrient"]
        },
        {
            "name": "choose_meal",
            "description": """Choose meal based on nutrient requirement and dietary restriction""",
            "parameters": {
                "type": "object",
                "properties": {
                    "nutrients": {
                        "type": "object",
                        "description": "denotes the quantities in grams of different nutrients in the meal"
                    },
                    "name": {
                        "type": "string",
                        "description": "unique name of the meal"
                    },
                    "recipe": {
                        "type": "object",
                        "description": "ingredients used to make the meal"
                    },
                    "restriction":{
                        "type":"string",
                        "description":"Dietary Restriction of customer"
                    }
                }
            },
            "required":["nutrients", "restriction"]
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        available_functions = {
            "get_recipe": get_recipe,
            "get_nutrients": get_nutrients,
            "get_and_compare_nutrients_between_2_meals":get_meals_and_compare_nutrients,
            "choose_meal":get_meal_based_on_restriction
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(function_args)

        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": str(function_response),
            }
        )
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response["choices"][0]["message"]["content"]
    else:
        return response_message["content"]



if __name__ == '__main__':
    # print(get_answer("what are the nutrients in the Chicken Pesto Pasta meal?"))
    # print(get_answer("I want to increase my protein intake, which meal would be better the Chickpea Meatloaf meal or Chicken Pesto Pasta Meal?"))
    # print(get_answer("what do I need to make the Chickpea Meatloaf Meal?"))
    # print(get_answer(
    #     "I want to decrease my calcium intake, which meal would be better the Chickpea Meatloaf meal or Chicken Pesto Pasta Meal?"))
    print(get_answer(
        "I have been recommended to increase my calcium intake but I am diabetic, which meal should I have?"))