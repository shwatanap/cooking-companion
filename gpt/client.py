from dataclasses import dataclass, field
from os import environ
from typing import List

import openai
from openai.openai_object import OpenAIObject

import config
from gpt.constants import Model
from gpt.message import Message


@dataclass
class ChatGPTClient:
    model: Model
    messages: List[Message] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not (key := config.CHATGPT_API_KEY):
            raise Exception(
                "chatGPT api key is not set as an environment variable"
            )
        openai.api_key = key

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def reset(self) -> None:
        self.messages = []

#オブジェクト生成
    def create(self) -> OpenAIObject:
        res = openai.ChatCompletion.create(
            max_tokens=500,
            model=self.model.value,
            messages=[m.to_dict() for m in self.messages],
        )
        #入力文一覧を出力
        print(self.messages)
        #返信を追加
        self.add_message(Message.from_dict(res["choices"][0]["message"]))
        return res
