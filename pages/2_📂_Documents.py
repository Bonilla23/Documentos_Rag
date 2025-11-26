import streamlit as st
from utils.styles import load_css
from utils.rag_engine import RAGEngine
import pandas as pd

st.set_page_config(page_title="Documents", page_icon="📂", layout="wide")
load_css()

st.title("📂 Advanced Document Management")

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

# Two column layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload New Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files", 
        type=["pdf", "txt"], 
        accept_multiple_files=True,
        help="Max file size: 1GB per file"
    )

    if uploaded_files:
        if st.button(f"🚀 Process {len(uploaded_files)} Files", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_chunks = 0
            for i, file in enumerate(uploaded_files):
                status_text.text(f"⚙️ Processing {file.name}...")
                try:
                    num_chunks = st.session_state.rag_engine.ingest_file(file)
                    total_chunks += num_chunks
                    st.toast(f"✅ {file.name} processed ({num_chunks} chunks)", icon="✅")
                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {str(e)}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✨ All files processed!")
            st.success(f"🎉 Successfully added **{total_chunks}** new chunks to the database.")
            st.balloons()

with col2:
    st.markdown("### 📊 Database Stats")
    
    if st.button("🔄 Refresh Stats", use_container_width=True):
        st.rerun()
        
    stats = st.session_state.rag_engine.db_manager.get_collection_stats()
    
    st.metric("Total Chunks", stats.get('count', 0), delta=None)
    
    # Show storage info
    st.markdown("**💾 Storage Location:**")
    st.code("./data/chroma_db", language="bash")
    
    st.divider()
    
    st.markdown("### 🗑️ Danger Zone")
    if st.button("⚠️ Reset Database", type="secondary", use_container_width=True):
        if st.checkbox("✅ Confirm Reset?"):
            st.session_state.rag_engine.db_manager.reset_db()
            st.success("🗑️ Database cleared!")
            st.rerun()

st.divider()

# Document Browser
st.markdown("### 📚 Document Browser")

stats = st.session_state.rag_engine.db_manager.get_collection_stats()
peek_data = stats.get("peek")

if peek_data and peek_data.get("ids"):
    # Create DataFrame
    ids = peek_data.get("ids", [])
    documents = peek_data.get("documents", [])
    metadatas = peek_data.get("metadatas", [])
    
    df_data = []
    for i, (doc_id, content, meta) in enumerate(zip(ids, documents, metadatas)):
        df_data.append({
            "ID": doc_id[:8] + "...",
            "Source": meta.get("source", "Unknown"),
            "Content Preview": content[:100] + "...",
            "Length": len(content)
        })
    
    df = pd.DataFrame(df_data)
    
    # Display with selection
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("Chunk ID", width="small"),
            "Source": st.column_config.TextColumn("Source File", width="medium"),
            "Content Preview": st.column_config.TextColumn("Preview", width="large"),
            "Length": st.column_config.NumberColumn("Chars", width="small")
        }
    )
    
    st.divider()
    
    # Document Details Viewer
    st.markdown("### 🔍 Document Details")
    
    selected_idx = st.selectbox(
        "Select a chunk to view details:",
        range(len(ids)),
        format_func=lambda x: f"Chunk {x+1}: {metadatas[x].get('source', 'Unknown')}"
    )
    
    if selected_idx is not None:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**Full Content:**")
            st.markdown(f"```\n{documents[selected_idx]}\n```")
        
        with col2:
            st.markdown("**Metadata:**")
            st.json(metadatas[selected_idx])
            
            st.markdown("**Chunk ID:**")
            st.code(ids[selected_idx], language="text")
    
else:
    st.info("📭 No documents in database. Upload some files to get started!")

st.divider()

# Quick Actions
st.markdown("### ⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Test Search", use_container_width=True):
        st.session_state.show_search = True

with col2:
    if st.button("📊 View Analytics", use_container_width=True):
        st.switch_page("pages/6_📊_Analytics.py")

with col3:
    if st.button("💬 Start Chatting", use_container_width=True):
        st.switch_page("pages/1_💬_Chat.py")

# Search Test Section
if st.session_state.get("show_search", False):
    st.divider()
    st.markdown("### 🔍 Search Test")
    
    query = st.text_input("Enter search query:", placeholder="What are you looking for?")
    
    if query:
        with st.spinner("Searching..."):
            results = st.session_state.rag_engine.vector_store.similarity_search(query, k=5)
            
            st.markdown(f"**Found {len(results)} results:**")
            
            for i, doc in enumerate(results, 1):
                with st.expander(f"📄 Result {i}: {doc.metadata.get('source', 'Unknown')}"):
                    st.markdown(doc.page_content)
                    st.caption(f"Source: {doc.metadata.get('source', 'Unknown')}")
