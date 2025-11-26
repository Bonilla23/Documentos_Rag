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
        model_name = st.selectbox("Model", ["gemini-2.5-pro", "gemini-2.5-flash"])
    else:
        default_model = os.getenv("OLLAMA_MODEL", "llama3")
        model_name = st.text_input("Ollama Model", value=default_model)
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    
    st.divider()
    
    # Reset Chat Button
    st.markdown("### 🗑️ Reset Chat")
    if st.button("🔄 Clear History", type="secondary", use_container_width=True):
        st.session_state.messages = []
        if "chain" in st.session_state:
            del st.session_state.chain  # Also clear chain to reset memory
        st.success("✅ Chat cleared!")
        st.rerun()

# Initialize or update chain when settings change
chain_key = f"{model_provider}_{model_name}_{temperature}"
if "chain_key" not in st.session_state or st.session_state.chain_key != chain_key or "chain" not in st.session_state:
    # Settings changed or chain not initialized, recreate chain
    with st.spinner("Initializing model..."):
        st.session_state.chain = st.session_state.rag_engine.get_chain(
            model_provider=model_provider,
            model_name=model_name,
            temperature=temperature
        )
        st.session_state.chain_key = chain_key

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
            with st.spinner("Thinking..."):
                # Use persisted chain
                result = st.session_state.chain.invoke({"question": prompt, "chat_history": []})
                response_text = result["answer"]
                
                # Real streaming effect (word by word)
                words = response_text.split()
                for i, word in enumerate(words):
                    full_response += word + " "
                    # Update every 3 words for smoother streaming
                    if i % 3 == 0 or i == len(words) - 1:
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.02)  # Minimal delay for visual effect
                message_placeholder.markdown(full_response)
                
                # Show sources
                if result.get("source_documents"):
                    with st.expander("📚 Sources"):
                        for i, doc in enumerate(result["source_documents"], 1):
                            st.markdown(f"**Source {i}: {doc.metadata.get('source', 'Unknown')}**")
                            st.markdown(f"```\n{doc.page_content[:300]}...\n```")

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
