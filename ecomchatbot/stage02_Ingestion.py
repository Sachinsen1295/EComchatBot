from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import pandas as pd
from ecomchatbot.Stage01_dataconverter import dataconveter


ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")

#from ecomchatbot.Stage01_dataconverter import dataconverter

def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings


embedding = download_hugging_face_embeddings()

def data_ingestion(status):
   vstore =  AstraDBVectorStore(
                embedding=embedding,
                collection_name="ecomchatbot",
                api_endpoint=ASTRA_DB_API_ENDPOINT,
                token=ASTRA_DB_APPLICATION_TOKEN,
                namespace=ASTRA_DB_KEYSPACE
            )
   
   storage = status

   if storage == None:
       docs = dataconveter()
       inserted_ids = vstore.add_documents(docs)
       
   else:
        return vstore
   
   return vstore, inserted_ids


if __name__ == '__main__':
    vstore,inserted_ids=data_ingestion(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound headset.")
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")



