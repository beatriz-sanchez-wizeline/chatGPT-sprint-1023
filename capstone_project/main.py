#!/usr/bin/env python3

from brain_module import ChatGPT
from inventionary import Inventionary

if __name__ == "__main__":
    bot = ChatGPT()
    promptBuilder = Inventionary(bot)
    user_prompt = promptBuilder.start()
    print(user_prompt)

    # bot = ChatGPT()
    # response = bot.request_openai("You are a skilled marketing expert", "Propose a business name")
    # print(response)
