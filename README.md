# Build and Deploy Your Personal ChatGPT Bot in Python with ChatGPT API in Mac


### INTRODUCTION

In today's digital age, chatbots have become essential for enhancing customer support, automating tasks, and delivering engaging user experiences. OpenAI's ChatGPT API, powered by the advanced gpt-3.5-turbo-16k model, offers a powerful solution for creating interactive chatbots. 

In this tutorial, I will guide you through building and deploying your own ChatGPT bot using just a few lines of Python code on your Mac. With this approach, your bot will even be able to consider and utilize local personal user data stored in various file formats to answer questions about you and the kind of data you store inside that directory locally. Isn't it awesome?


### USEFUL LINK

https://platform.openai.com/playground?mode=chat&model=gpt-3.5-turbo-16k

https://platform.openai.com/docs/guides/gpt


### PRE-REQUISITES

Before diving into the implementation, ensure you have the following:
A Mac computer (this tutorial is specifically tailored for macOS users)

  1) Python 3.7 or higher installed  
  2) Basic knowledge of Python programming
  3) An OpenAI account with access to the ChatGPT API


### Step 1: Setting Up the Environment

We need to set up a Python environment and install the necessary libraries. Open a terminal and create a new directory for your project.

```shell

$ mkdir chatgpt-bot
$ cd chatgpt-bot

```

Here, we will use the three crucial libraries: ```OpenAI```,```textract```, and ```glob``` to implement this.
OpenAI is a leading artificial intelligence research organization that has developed the [ChatGPT API](https://platform.openai.com/docs/api-reference), which allows us to interact with the powerful ChatGPT model. With the OpenAI API, we can send prompts and receive responses from the ChatGPT model, enabling us to create conversational chatbots.
You can learn more about OpenAI and its offerings here.

The second textract Python library package provides text extraction capabilities from various file formats. It supports a wide range of file formats, including but not limited to:
  1. Text-based formats: TXT, CSV, JSON, XML, HTML, Markdown, and LaTeX.
  2. Document formats: DOC, DOCX, XLS, XLSX, PPT, PPTX, ODT, and ODS.
  3. eBook formats: EPUB, MOBI, AZW, and FB2.
  4. Image formats with embedded text: JPG, PNG, BMP, GIF, TIFF, and PDF (both searchable and scanned).
  4. Programming source code files: Python, C, C++, Java, JavaScript, PHP, Ruby, and more.

The ```glob``` package in Python is a built-in module that provides a convenient way to search for files and directories using pattern matching. It allows you to find files that match a specified pattern, such as all files with a particular extension or files with specific naming patterns.
Next, let's install the required Python libraries:

```shell
$ pip install openai textract glob
```

### Step 2: Obtaining OpenAI API Access

To use the ChatGPT API, you'll need an [OpenAI API key](https://platform.openai.com/account/api-keys). If you don't have one, sign in to your OpenAI account and generate an API key from the dashboard.

Once you have the API key, save it securely as an environment variable in your terminal:

```python
export OPENAI_API_KEY='your-api-key'
```

### Step 3: Create a /data Directory in the project's current working directory to store your data:

Add all personal files there, containing anything from .txt to any .csv, or bot.docx files. The model will use the data inside this directory to answer  your personal questions based on the data you store here. For example, I have created a .txt file inside this directory and added my resume.

<img width="450" alt="Screenshot 2023-07-16 at 5 47 20 PM" src="https://github.com/anishsingh20/Personal-ChatGPT-Bot-For-Mac/assets/15655876/86dbba3d-2c24-4252-9cd0-4d4e85d449ea">

<img width="450" alt="Screenshot 2023-07-16 at 5 45 24 PM" src="https://github.com/anishsingh20/Personal-ChatGPT-Bot-For-Mac/assets/15655876/58848d85-ca4c-4e40-87f5-68d6ca4830c2">


### Step 4: Building the ChatGPT Bot

Now, let's write the code for our ChatGPT bot. Create a new Python file, such as ```chatGPTbot.py```, and add the following code:

```python

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

```

```append_to_chat_history(message)```: This function appends the user's message to the chat history stored in the chat_history list.

```read_personal_file(file_path)```: This function utilizes the ```textract``` library to extract text from personal files. It attempts to decode the extracted text using UTF-8 encoding. An error message is displayed if any errors occur during the extraction process.

```collect_user_data()```: This function collects the user's data stored in the "/data" directory, placed inside the current working directory. It iterates through the files in the directory, determines their file types, and uses the appropriate method to extract text. It returns the combined user data as a string.

```create_chat_response(message)```: This function constructs the chat response using the OpenAI ChatCompletion API. It appends the user's message and the collected user data (if any) to the message list. The API call is made with the provided messages, and the response is stored in the response variable. The function then appends the response to the chat history and returns it.

```start_chatting()```: This function initiates an interactive chat session with the user. It prompts the user for input, generates the bot's response using create_chat_response(), and prints the response. The conversation continues until the user enters "exit" to quit.

In a nutshell:

In the end, the while True loop continuously prompts the user for input. ***To exit the chatbot, type "exit."***


### Step 5: Deploying the ChatGPT Bot

To run the program, you must open a terminal and execute the Python file. In your terminal, run the following command:

```shell
$ python chatGPTbot.py
Or
$ python3 chatGPTbot.py
```
<img width="821" alt="Screenshot 2023-07-16 at 5 29 53 PM" src="https://github.com/anishsingh20/Personal-ChatGPT-Bot-For-Mac/assets/15655876/1ebab853-2bf2-495b-bd76-cb469b75b03d">





Voila! Your personal ChatGPT bot is now ready to chat. You can start interacting with it by entering messages, and the bot will respond accordingly. When you're finished, simply type "exit" to end the conversation.
