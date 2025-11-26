import streamlit as st
from utils.styles import load_css
import os

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
load_css()

st.title("⚙️ Settings")

st.markdown("### 🔑 API Keys")

api_key = st.text_input(
    "Google Gemini API Key", 
    type="password", 
    value=os.getenv("GOOGLE_API_KEY", ""),
    help="Required for Gemini models and embeddings."
)

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    # Save to .env
    with open(".env", "w") as f:
        f.write(f"GOOGLE_API_KEY={api_key}\n")
    st.success("API Key saved to .env!")
else:
    st.warning("No Google API Key found. Gemini features will not work.")

st.markdown("### 🦙 Ollama Configuration")
ollama_url = st.text_input("Ollama Base URL", value=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
ollama_model = st.text_input("Ollama Chat Model", value=os.getenv("OLLAMA_MODEL", "llama3"), help="e.g., gemma2, llama3, mistral")
ollama_embedding = st.text_input("Embedding Model (Sentence Transformers)", value=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"), help="HuggingFace model name (e.g., all-MiniLM-L6-v2, intfloat/multilingual-e5-large)")

if st.button("Save Configuration"):
    os.environ["OLLAMA_HOST"] = ollama_url
    os.environ["OLLAMA_MODEL"] = ollama_model
    os.environ["EMBEDDING_MODEL"] = ollama_embedding
    
    # Update .env safely
    env_content = {}
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        env_content[k] = v
        except UnicodeDecodeError:
            pass
            
    env_content["OLLAMA_HOST"] = ollama_url
    env_content["OLLAMA_MODEL"] = ollama_model
    env_content["EMBEDDING_MODEL"] = ollama_embedding
    
    # Ensure GOOGLE_API_KEY is preserved if not in env_content but in os.environ
    if "GOOGLE_API_KEY" not in env_content and os.getenv("GOOGLE_API_KEY"):
        env_content["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    with open(".env", "w", encoding="utf-8") as f:
        for k, v in env_content.items():
            f.write(f"{k}={v}\n")
            
    st.success("Ollama configuration saved to .env!")

st.markdown("### 🎨 Appearance")
theme = st.selectbox("Theme", ["Dark (Default)", "Light"])
if theme == "Light":
    st.info("To switch to Light mode, please change the theme in Streamlit's top-right menu settings.")

st.divider()
st.markdown("### ℹ️ About")
st.markdown("Built with **Streamlit**, **LangChain**, **ChromaDB**, **Gemini**, and **Ollama**.")
st.markdown("Version 1.0.0")
