import os
import glob
import openai
import textract

class Chatbot:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.chat_history = []

    def append_to_chat_history(self, message):
        self.chat_history.append(message)

    def read_personal_file(self, file_path):
        try:
            text = textract.process(file_path).decode("utf-8")
            return text
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    def collect_user_data(self):
        data_directory = "./data"
        data_files = glob.glob(os.path.join(data_directory, "*.*"))

        user_data = ""
        for file in data_files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in (".pdf", ".docx", ".xlsx", ".xls"):
                user_data += self.read_personal_file(file)
            else:
                with open(file, "r", encoding="utf-8") as f:
                    user_data += f.read() + "\n"

        return user_data

    def create_chat_response(self, message):
        self.append_to_chat_history(message)

        user_data = self.collect_user_data()
        messages = [
            {"role": "system", "content": "You are the most helpful assistant."},
            {"role": "user", "content": message},
            {"role": "assistant", "content": message},
        ]

        if user_data:
            messages.append({"role": "user", "content": user_data})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
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
