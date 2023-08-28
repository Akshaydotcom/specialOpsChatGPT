import openai
import json



from main import insert_quantity

messages2 = [{"role": "system", "content": "You are a helpful personal assistant to doctor Seuss who is calling a "
                                           "pharmacy to ask if they have 20mg instant release adderall in stock. You "
                                           "only want to know if they have the drug and if yes, how much is available "
                                           "on hand right now. Do not ask to purchase any, if asked for help with "
                                           "anything else, decline politely and end the conversation"}]


def getData(reply):
    messages = [{'role': 'user', 'content': reply}]
    functions = [
        {
            "name": "inputDataIntoDB",
            "description": """Enter the quantity of the drug based on the string""",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "unique name of the drug"
                    },
                    "quantity": {
                        "type": "number",
                        "description": "quantity of drug in stock"
                    }
                }
            },
            "required": ["name", "quantity"]
        },
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
            "inputDataIntoDB": insert_quantity
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


def analyze_conversation(messages):
    m = [{"role": "system",
          "content": "You are a transcriber who has been asked to read conversation between a doctors "
                     "PA and a pharmacy and help extract the name of the drug and the quantity mentioned in the "
                     "conversation between a Personal Assistant (PA) and a Pharmacy. Do not complete the conversation, only read and extract data"}]
    content = ""
    for message in messages[1:]:
        content += message.get('content')

    if messages:
        m.append({"role": "user", "content": content})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=m
        )
        reply = chat.choices[0].message.content
        return reply


def chatbot(input):
    if input:
        messages2.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages2
        )
        reply = chat.choices[0].message.content
        messages2.append({"role": "assistant", "content": reply})
        return reply


print('This is the pharmacy, how may I help you?')
print(chatbot('This is the pharmacy, how may I help you?'))
print('Yes, we have it in stock')
print(chatbot('Yes, we have it in stock'))
print('Hold, on let me check')
print(chatbot('Hold, on let me check'))
print('Yes, we currently have 35 packets')
print(chatbot('Yes, we currently have 35 packets'))
reply=(analyze_conversation(messages2))
getData(reply)
# print(chatbot('Thanks for holding, what can I help you with?'))
