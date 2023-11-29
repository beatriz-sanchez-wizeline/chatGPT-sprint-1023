#!/usr/bin/env python3

import os
from openai import OpenAI
from dotenv import load_dotenv


class ChatGPT:
    """A class to interact with OpenAI's ChatGPT model."""

    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

        # Retrieve the OPENAI_API_KEY environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")

        # Set the retrieved API key for the OpenAI library
        self.client = OpenAI(api_key=self.api_key)

        # A constant to describe the role or behavior of the chatbot
        self.MAIN_ROLE = "This is the behavior of chatGPT"

    def request_openai(self, messages):
        """
        Make a request to the OpenAI API.

        Args:
        - messages (array): The list of messages to be sent to the OpenAI API. [{role: <role>, message: <message}, ...]

        Returns:
        - str: The response from the OpenAI API.
        """

        # Create a chat completion with the provided message and role
        return self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

    def close_client(self):
        """
        Make a request to the OpenAI API.

        Args:
        - messages (array): The list of messages to be sent to the OpenAI API. [{role: <role>, message: <message}, ...]

        Returns:
        - str: The response from the OpenAI API.
        """

        # Create a chat completion with the provided message and role
        return self.client.close()

# If you need to test or use this directly, you can do:
# if __name__ == "__main__":
#     chat_gpt = ChatGPT()
#     print(chat_gpt.request_openai("Hello!"))
