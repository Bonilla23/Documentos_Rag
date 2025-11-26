import streamlit as st
from utils.styles import load_css, card
from utils.rag_engine import RAGEngine

st.set_page_config(page_title="Documents", page_icon="📂", layout="wide")
load_css()

st.title("📂 Document Management")

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Upload New Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files", 
        type=["pdf", "txt"], 
        accept_multiple_files=True,
        help="Max file size: 1GB per file"
    )

    if uploaded_files:
        if st.button(f"Process {len(uploaded_files)} Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_chunks = 0
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                try:
                    num_chunks = st.session_state.rag_engine.ingest_file(file)
                    total_chunks += num_chunks
                    st.toast(f"✅ {file.name} processed ({num_chunks} chunks)")
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("All files processed!")
            st.success(f"Successfully added {total_chunks} new chunks to the database.")

with col2:
    st.markdown("### 📊 Database Stats")
    # We can't easily get real-time stats without querying the DB every time.
    # Let's add a refresh button or just show what we know.
    
    if st.button("Refresh Stats"):
        st.rerun()
        
    stats = st.session_state.rag_engine.db_manager.get_collection_stats()
    
    card("Total Documents", f"{stats.get('count', 0)} chunks")
    
    st.markdown("### 🗑️ Management")
    if st.button("Reset Database (Clear All)", type="secondary"):
        if st.checkbox("Confirm Reset?"):
            st.session_state.rag_engine.db_manager.reset_db()
            st.success("Database cleared!")
            st.rerun()
