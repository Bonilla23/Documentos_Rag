import streamlit as st
from utils.styles import load_css, card
from dotenv import load_dotenv
import os
import warnings

# Suppress warnings for cleaner console
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*torch.classes.*')
warnings.filterwarnings('ignore', module='langchain')

load_dotenv()

st.set_page_config(
    page_title="Documentos RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

st.title("🤖 Documentos RAG")
st.markdown("### Advanced Retrieval Augmented Generation System")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    Welcome to your **Spectacular RAG Application**. This system allows you to:
    
    *   **📄 Upload Documents**: Support for PDF and TXT files (up to 1GB).
    *   **🔍 Vector Search**: Powered by ChromaDB and Advanced Embeddings.
    *   **🧠 Multi-Model Support**: Switch between **Gemini** (Cloud) and **Ollama** (Local).
    *   **💬 Interactive Chat**: Context-aware conversations with your data.
    
    Get started by uploading documents in the **Documents** page!
    """)
    
    st.info("💡 Tip: Go to Settings to configure your API Keys and Models.")

with col2:
    card("🚀 Quick Stats", """
    - **System**: Online
    - **Database**: ChromaDB
    - **Models**: Gemini / Ollama
    """)
    
    if st.button("📂 Go to Uploads", use_container_width=True):
        st.switch_page("pages/2_📂_Documents.py")
    
    if st.button("💬 Start Chatting", use_container_width=True):
        st.switch_page("pages/1_💬_Chat.py")
