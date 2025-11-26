import chromadb
import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st

class DBManager:
    def __init__(self, persist_directory="./data/chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)

    def get_embedding_function(self):
        # Use local Sentence Transformers by default (no API limits)
        # Only use Gemini if explicitly configured
        use_gemini = os.getenv("USE_GEMINI_EMBEDDINGS", "false").lower() == "true"
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if use_gemini and api_key:
            return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        else:
            # Use a lightweight, high-quality default model (no quota limits)
            model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
            return HuggingFaceEmbeddings(model_name=model_name, model_kwargs={'device': 'cpu'})

    def get_vector_store(self, collection_name="documents"):
        embedding_function = self.get_embedding_function()
        return Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=embedding_function,
        )

    def get_collection_stats(self, collection_name="documents"):
        try:
            collection = self.client.get_collection(collection_name)
            return {
                "count": collection.count(),
                "peek": collection.peek()
            }
        except ValueError:
            return {"count": 0, "peek": None}

    def reset_db(self):
        self.client.reset()
