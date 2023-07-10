# Personal-ChatGPT-Bot-For-Mac

Create and deploy your chatGPT bot written in Python using the [ChatGPT API](https://platform.openai.com/account/api-keys), [LangChain](https://python.langchain.com/docs/get_started/quickstart), and just a few lines of code. 

Follow along fellas, for some magic. 

1) Easy to setup
2) Train on whatever data you want and OpenAI data using the OpenAI API.
3) Use the best of both worlds


***DISCLAIMER: PLEASE DO NOT USE ANY SENSITIVE PERSONAL DATA TO TRAIN THE MODEL***


------



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


3) Place your data into ```data/My_data.txt```.




4) Now create another Python file in the same working directory, which will contain all the code and necessary modules -- ***REAL MAGIC HAPPENS HERE*** -- ```my_chatGPT_bot.py```

   ```python
   
      import os
      import sys
      
      import openai
      from langchain.chains import ConversationalRetrievalChain, RetrievalQA
      from langchain.chat_models import ChatOpenAI
      from langchain.document_loaders import DirectoryLoader, TextLoader
      from langchain.embeddings import OpenAIEmbeddings
      from langchain.indexes import VectorstoreIndexCreator
      from langchain.indexes.vectorstore import VectorStoreIndexWrapper
      from langchain.llms import OpenAI
      from langchain.vectorstores import Chroma
      
      import openai_apikey  # importing the chatGPT API key
      
      os.environ["OPENAI_API_KEY"] = openai_apikey.APIKEY

      # Enable to save to disk & reuse the model (for repeated queries on the same data)
      PERSIST = False
      
      query = None
      if len(sys.argv) > 1:
        query = sys.argv[1]
      
      if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
      else:
        #loader = TextLoader("data/My_data.txt") # Use your data as if you only need My_data.txt
        loader = DirectoryLoader("data/")  # use the complete directory for data to train on
        if PERSIST:
          index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
          index = VectorstoreIndexCreator().from_loaders([loader])
      
      chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
      )
      
      chat_history = []
      while True:
        if not query:
          query = input("Prompt: ")
        if query in ['quit', 'q', 'exit']:
          sys.exit()
        result = chain({"question": query, "chat_history": chat_history})
        print(result['answer'])
      
        chat_history.append((query, result['answer']))
        query = None


    

   
   ```
