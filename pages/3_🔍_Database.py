import streamlit as st
from utils.styles import load_css
from utils.rag_engine import RAGEngine
import pandas as pd

st.set_page_config(page_title="Database Inspector", page_icon="🔍", layout="wide")
load_css()

st.title("🔍 Database Inspector")

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

stats = st.session_state.rag_engine.db_manager.get_collection_stats()
st.metric("Total Chunks", stats.get("count", 0))

st.markdown("### Peek at Data")
st.markdown("View the first few items in the vector database.")

peek_data = stats.get("peek")
if peek_data:
    # Convert to DataFrame for nicer display
    # Chroma peek returns dict of lists
    ids = peek_data.get("ids", [])
    documents = peek_data.get("documents", [])
    metadatas = peek_data.get("metadatas", [])
    
    if ids:
        df = pd.DataFrame({
            "ID": ids,
            "Content": documents,
            "Source": [m.get("source", "Unknown") for m in metadatas]
        })
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Database is empty.")
else:
    st.info("No data found or database empty.")

st.markdown("### Search Test")
query = st.text_input("Test Query", "What is...")
if query:
    results = st.session_state.rag_engine.vector_store.similarity_search(query, k=3)
    for i, doc in enumerate(results):
        with st.expander(f"Result {i+1} (Source: {doc.metadata.get('source', 'Unknown')})"):
            st.markdown(doc.page_content)
