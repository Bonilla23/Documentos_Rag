import os
import tempfile
from typing import List
import warnings

# Suppress LangChain deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='langchain')

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from utils.db_manager import DBManager

class RAGEngine:
    def __init__(self):
        self.db_manager = DBManager()
        self.vector_store = self.db_manager.get_vector_store()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def ingest_file(self, uploaded_file):
        """Ingests a file (PDF or TXT) into the vector database."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            if uploaded_file.name.endswith(".pdf"):
                loader = PyPDFLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path)
            
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata["source"] = uploaded_file.name
            
            self.vector_store.add_documents(chunks)
            return len(chunks)
        finally:
            os.remove(tmp_path)

    def get_llm(self, model_provider, model_name, temperature=0.7):
        if model_provider == "Gemini":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API Key not found.")
            return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=temperature)
        elif model_provider == "Ollama":
            return ChatOllama(model=model_name, temperature=temperature)
        else:
            raise ValueError("Invalid model provider")

    def get_chain(self, model_provider="Gemini", model_name="gemini-2.5-flash", temperature=0.7):
        llm = self.get_llm(model_provider, model_name, temperature)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=True
        )
        return chain
