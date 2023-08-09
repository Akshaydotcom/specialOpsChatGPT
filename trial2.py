
import openai
import json
from main import get_recipe
from main import get_nutrients
openai.api_key = ""


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
        },{
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
            "get_nutrients": get_nutrients
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
    print(get_answer("I need to get more protein, which meal would be better the Chicken Pesto Pasta or the Chickpea Meatloaf?"))
    # print(get_answer("what do I need to make the Chicken Pesto Pasta meal?"))