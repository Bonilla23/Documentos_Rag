import streamlit as st
from utils.styles import load_css
import json

st.set_page_config(page_title="History", page_icon="📜", layout="wide")
load_css()

st.title("📜 Chat History")

if "messages" not in st.session_state or not st.session_state.messages:
    st.info("No chat history available yet.")
else:
    st.markdown("### Current Session")
    for msg in st.session_state.messages:
        role = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
        with st.chat_message(msg["role"]):
            st.write(f"**{role}**: {msg['content']}")
            
    st.divider()
    
    # Export options
    st.markdown("### Export")
    history_json = json.dumps(st.session_state.messages, indent=2)
    st.download_button(
        label="Download History (JSON)",
        data=history_json,
        file_name="chat_history.json",
        mime="application/json"
    )
