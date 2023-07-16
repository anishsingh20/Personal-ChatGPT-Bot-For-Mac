# Build and Deploy Your Personal ChatGPT Bot in Python with ChatGPT API, LangChain for Mac


### INTRODUCTION


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

We need to set up a Python environment and install the necessary libraries. Open a terminal and create a new directory for your project. Once inside the project directory, create a virtual environment by running the following commands:


```shell

$ mkdir chatgpt-bot
$ cd chatgpt-bot
$ python3 -m venv venv
$ source venv/bin/activate

```

Here, we will use two crucial libraries: [OpenAI](https://platform.openai.com/) and [LangChain](https://github.com/hwchase17/langchain).

OpenAI is a leading artificial intelligence research organization that has developed the ChatGPT API, which allows us to interact with the powerful ChatGPT model. With the OpenAI API, we can send prompts and receive responses from the ChatGPT model, enabling us to create conversational chatbots.
You can learn more about OpenAI and its offerings [here](https://openai.com/).

LangChain is a Python library that provides utility functions for handling text-based inputs and outputs when working with OpenAI's language models. It helps with tokenization, text formatting, and managing conversational context. LangChain simplifies constructing prompt chains for conversations with the ChatGPT model. You can find more information about LangChain here.

By installing both OpenAI and LangChain, we have all the necessary tools to build our ChatGPT bot. Let's proceed to the next steps and bring our chatbot to life!
Next, let's install the required Python libraries:

```shell
$ pip install openai langchain
```

### Step 2: Obtaining OpenAI API Access

To use the ChatGPT API, you'll need an [OpenAI API key](https://platform.openai.com/account/api-keys). If you don't have one, sign in to your OpenAI account and generate an API key from the dashboard.

Once you have the API key, save it securely as an environment variable in your terminal:

```python
export OPENAI_API_KEY='your-api-key'
```

### Step 3: Building the ChatGPT Bot

Now, let's write the code for our ChatGPT bot. Create a new Python file, such as ```chatbot.py```, and add the following code:

```python
import openai
from langchain import LangChain
import os
import glob

def create_chatbot():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    langchain = LangChain()

    def get_chat_response(message):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=langchain.chain(message),
            temperature=0.8,
            max_tokens=50,
            n=1,
            stop=None,
            log_level="info",
        )
        return response.choices[0].text.strip()

    def import_personal_data(directory):
        supported_extensions = [".txt", ".docx", ".xlsx"]
        for file_path in glob.glob(f"{directory}/*"):
            file_extension = os.path.splitext(file_path)[1]
            if file_extension in supported_extensions:
                with open(file_path, "r") as file:
                    personal_data = file.read()
                    langchain.add_text(personal_data)
            else:
                print(f"Warning: Skipping unsupported file '{file_path}'")

    # Specify the directory containing your personal data files
    personal_data_directory = "personal_data"

    # Import and add your personal data from various file types
    import_personal_data(personal_data_directory)

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        bot_response = get_chat_response(user_input)
        print("Chatbot:", bot_response)

```

In a gist, this code defines a create_chatbot() function that initializes the OpenAI API key and the LangChain utility. 
The ```get_chat_response()``` function sends a user message to the ChatGPT model and returns the generated response.

We added an ```import_personal_data()``` function that takes the directory path as a parameter. It uses the glob module to iterate over the files in the specified directory. For each file, it checks if the file extension matches one of the supported extensions (e.g., .txt, .docx, .xlsx). If a file is compatible, its contents are read and added to the LangChain instance using ```langchain.add_text()```.

We also added an additional else block inside the ```import_personal_data()``` function. If a file has an unsupported extension, it will print a warning message indicating the unsupported file and continue to the next file. This way, you'll receive feedback about the skipped files and can ensure that your personal data consists of supported file types.

To use this functionality, create a directory named ```"personal_data"``` in the project's current working directory and place your files with compatible extensions (e.g., text files, Excel files, Word documents) inside it. The code will scan the directory and incorporate the contents of those files into the LangChain instance.

With this code, your ChatGPT bot can train and answer queries based on data from various file types. It provides a personalized experience that leverages your data across different file formats. Enjoy exploring and interacting with your enhanced ChatGPT bot!

At the end, the while True loop continuously prompts the user for input. ***To exit the chatbot, type "exit."***


### Step 4: Deploying the ChatGPT Bot

We need to create an executable script to deploy our chatbot as a command-line tool. In your terminal, run the following command:

```shell
$ chmod +x chatbot.py
```

This command gives the script executable permissions. Now, you can run the chatbot by executing the following command:

```shell
$ ./chatbot.py
```

Voila! Your personal ChatGPT bot is now ready to chat. Start interacting with it by entering messages, and the bot will respond accordingly. When you're finished, simply type "exit" to end the conversation.
