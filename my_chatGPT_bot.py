
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


 

