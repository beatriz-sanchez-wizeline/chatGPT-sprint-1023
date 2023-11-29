#!/usr/bin/env python3

from brain_module import ChatGPT
from inventionary import Inventionary

if __name__ == "__main__":
    bot = ChatGPT()
    Inventionary(bot).start()


