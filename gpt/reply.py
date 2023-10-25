from gpt.client import ChatGPTClient
from gpt.constants import Model, Role
from gpt.message import Message

def create_recipe(input) -> str:
    client = ChatGPTClient(model=Model.GPT35TURBO)

    client.add_message(
        message=Message(role=Role.USER,
        content=input),
    )

    res = client.create()
    res_text = res["choices"][0]["message"]["content"]

    return res_text
