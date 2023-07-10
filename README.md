# Personal-ChatGPT-Bot-For-Mac

Create and deploy your chatGPT bot written in Python using the ChatGPT API, LangChain, and just a few lines of code.

1) Easy to setup
2) Train on whatever data you want and OpenAI data using the OpenAI API.
3) Use the best of both worlds


***DISCLAIMER: PLEASE DO NOT USE ANY SENSITIVE PERSONAL DATA TO TRAIN THE MODEL***



## SETTING-UP

Some details on setting up [Langchain](https://python.langchain.com/docs/get_started/quickstart)

1) Install [Langchain](https://python.langchain.com/docs/get_started/quickstart) and other required packages on Mac using ```pip```, open ```Terminal``` on Mac and follow along:

  ```
pip install langchain openai chromadb tiktoken unstructured
  ```

2) Create a new Python file on your local directory on Mac by the name ```~/openai_apikey.py``` and copy and paste your generated [OpenAI API](https://platform.openai.com/account/api-keys) key.

```
# ~/openai_apikey.py

# Replace your own generated OpenAI API Key https://platform.openai.com/account/api-keys
# and rename this file to openai_apikey.py.
APIKEY = "<your OpenAI API key>"
```
