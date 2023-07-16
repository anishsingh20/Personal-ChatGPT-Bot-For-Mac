

import os
import openai

class Chatbot:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.chat_history = []

    def append_to_chat_history(self, message):
        self.chat_history.append(message)

    def create_chat_response(self, message):
        self.append_to_chat_history(message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[ {"role": "system", "content": "You are the most helpful assistant."},
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": message}],
            temperature=1,
            max_tokens=256,
            top_p=1,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
            )

        self.append_to_chat_history(response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()

    def start_chatting(self):
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                print("Chatbot: Goodbye!")
                break
            bot_response = self.create_chat_response(user_input)
            print("Chatbot:", bot_response)

# Create an instance of the Chatbot class and start the conversation
chatbot = Chatbot()
chatbot.start_chatting()

