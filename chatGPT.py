import os
import openai
import json
from langchain.chat_models import ChatOpenAI

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def get_nutrition_data():
    with open('data.json','r') as json_file:
        sample_load=json.load(json_file)
    return sample_load

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "Shall we play a game?"}]
    functions = [
        {
            "name": "get_nutrition_data",
            "description": "Get the nutrition data about all meals",
            "parameters":{
                "type":"object"
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

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        print("Reached")
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        # available_functions = {
        #     "get_nutrition_data": get_nutrition_data,
        # }  # only one function in this example, but you can have multiple
        # function_name = response_message["function_call"]["name"]
        # function_to_call = available_functions[function_name]
        # function_response = function_to_call()

        # Step 4: send the info on the function call and function response to GPT
        # messages.append(response_message)  # extend conversation with assistant's reply
        # messages.append(
        #     {
        #         "role": "function",
        #         "name": function_name,
        #         "content": function_response,
        #     }
        # )  # extend conversation with function response
        # second_response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo-0613",
        #     messages=messages,
        # )  # get a new response from GPT where it can see the function response
        # return second_response


chat = ChatOpenAI(openai_api_key="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")
#
# chat([HumanMessage(
#     content="If I give you some data about food, can you tell me if I should eat on basis of nutritional values?")])
print(run_conversation())

# print(get_nutrition_data())