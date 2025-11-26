import streamlit as st
from utils.styles import load_css
from utils.rag_engine import RAGEngine
import time
import os

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")
load_css()

st.title("💬 Chat with Documents")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

# Sidebar Settings
with st.sidebar:
    st.header("Model Settings")
    model_provider = st.selectbox("Provider", ["Gemini", "Ollama"], index=0)
    
    if model_provider == "Gemini":
        model_name = st.selectbox("Model", ["gemini-pro", "gemini-1.5-flash"])
    else:
        default_model = os.getenv("OLLAMA_MODEL", "llama3")
        model_name = st.text_input("Ollama Model", value=default_model)
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask something about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            chain = st.session_state.rag_engine.get_chain(
                model_provider=model_provider,
                model_name=model_name,
                temperature=temperature
            )
            
            # We need to pass chat history properly if we want memory, 
            # but for now let's just pass the question for simplicity in this turn
            # or reconstruct history.
            # The chain has memory built-in but it's a new chain instance every time here.
            # Ideally we persist the chain or memory.
            # For this "spectacular" app, let's just run the chain.
            
            with st.spinner("Thinking..."):
                result = chain.invoke({"question": prompt, "chat_history": []}) # Passing empty history for now to avoid complexity with types
                response_text = result["answer"]
                
                # Simulate typing effect
                for chunk in response_text.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # Show sources
                if result.get("source_documents"):
                    with st.expander("📚 Sources"):
                        for doc in result["source_documents"]:
                            st.markdown(f"**{doc.metadata.get('source', 'Unknown')}**: {doc.page_content[:200]}...")

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
