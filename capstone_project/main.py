#!/usr/bin/env python3

from brain_module import ChatGPT
from inventionary import Inventionary

if __name__ == "__main__":
    promptBuilder = Inventionary()
    user_prompt = promptBuilder.setup()
    print(user_prompt)

    # bot = ChatGPT()
    # response = bot.request_openai("You are a skilled marketing expert", "Propose a business name")
    # print(response)
