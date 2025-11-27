# 🤖 Documentos RAG

**Advanced Retrieval Augmented Generation System**

A spectacular, production-ready RAG (Retrieval Augmented Generation) application built with Streamlit, LangChain, and ChromaDB. Upload your documents and chat with them using powerful AI models like Google Gemini or local Ollama models.

![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue)
![Streamlit](https://img.shields.io/badge/streamlit-%3E%3D1.32.0-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- 📄 **Document Upload**: Support for PDF and TXT files (up to 1GB)
- 🔍 **Vector Search**: Powered by ChromaDB with Sentence Transformers embeddings
- 🧠 **Multi-Model Support**: 
  - **Gemini** (Cloud-based Google AI)
  - **Ollama** (Local models like Llama, Mistral, etc.)
- 💬 **Interactive Chat**: Context-aware conversations with your documents
- 📊 **Analytics Dashboard**: Visualize document statistics and usage patterns
- 🗄️ **Database Inspector**: Browse and manage your vector database
- 📜 **Chat History**: Review past conversations
- ⚙️ **Settings Panel**: Easy configuration of API keys and models
- 🎨 **Modern UI**: Beautiful, responsive interface with custom styling

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- (Optional) Ollama installed for local models
- (Optional) Google API key for Gemini models

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Documentos_Rag
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```
   
   Or using `uv` (recommended):
   ```bash
   uv pip install -e .
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
Documentos_Rag/
├── main.py                 # Main application entry point
├── pages/                  # Streamlit multipage app
│   ├── 1_💬_Chat.py       # Chat interface
│   ├── 2_📂_Documents.py  # Document upload & management
│   ├── 3_🔍_Database.py   # Vector database inspector
│   ├── 4_📜_History.py    # Chat history viewer
│   ├── 5_⚙️_Settings.py   # Configuration panel
│   └── 6_📊_Analytics.py  # Analytics dashboard
├── utils/                  # Utility modules
│   ├── rag_engine.py      # RAG core logic
│   ├── db_manager.py      # Database operations
│   ├── analytics.py       # Analytics functions
│   └── styles.py          # Custom CSS styling
├── data/                   # Data storage
│   └── chroma_db/         # ChromaDB vector store
├── .env                    # Environment variables (create this)
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

---

## 🔧 Configuration

### Using Gemini (Cloud)

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```
3. Select "Gemini" in the Settings page

### Using Ollama (Local)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. Select "Ollama" in the Settings page and choose your model

---

## 📖 Usage Guide

### 1. Upload Documents

1. Navigate to **📂 Documents** page
2. Click "Browse files" or drag & drop your PDF/TXT files
3. Wait for processing (documents are automatically chunked and embedded)
4. View uploaded documents in the database

### 2. Chat with Your Documents

1. Go to **💬 Chat** page
2. Select your preferred model (Gemini or Ollama)
3. Type your question in the chat input
4. The system will retrieve relevant context and generate answers

### 3. Explore Analytics

1. Visit **📊 Analytics** page
2. View document statistics, token usage, and performance metrics
3. Analyze trends and patterns in your data

### 4. Manage Database

1. Open **🔍 Database** page
2. Browse stored documents and embeddings
3. Delete specific documents if needed

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit |
| **LLM Integration** | LangChain |
| **Vector Database** | ChromaDB |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **AI Models** | Google Gemini, Ollama (Llama, Mistral, etc.) |
| **Document Processing** | PyPDF, LangChain Text Splitters |
| **Visualization** | Plotly, Pandas |

---

## 🧩 Key Dependencies

```toml
streamlit>=1.32.0
langchain>=0.1.0
langchain-community>=0.0.20
langchain-google-genai>=0.0.9
langchain-ollama>=0.0.1
langchain-chroma>=0.1.0
langchain-huggingface>=0.0.1
sentence-transformers>=2.5.0
chromadb>=0.4.22
pypdf>=4.0.0
python-dotenv>=1.0.1
```

See [`pyproject.toml`](pyproject.toml) for the complete list.

---

## 🎯 Features in Detail

### RAG Engine

The core RAG engine (`utils/rag_engine.py`) handles:
- Document chunking with configurable chunk size and overlap
- Vector embeddings using Sentence Transformers
- Similarity search with ChromaDB
- Context retrieval and prompt engineering
- Multi-model LLM support

### Database Manager

The database manager (`utils/db_manager.py`) provides:
- Document storage and retrieval
- Metadata management
- Collection statistics
- Document deletion and cleanup

### Analytics

The analytics module (`utils/analytics.py`) offers:
- Document count and size tracking
- Token usage statistics
- Performance metrics
- Interactive visualizations

---

## 🔒 Security & Privacy

- API keys are stored in `.env` files (not committed to version control)
- Local Ollama models keep your data completely private
- ChromaDB data is stored locally in `data/chroma_db/`
- No data is sent to external services when using Ollama

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `UnicodeDecodeError` when processing documents
- **Solution**: Ensure your documents are properly encoded (UTF-8)

**Issue**: Ollama connection error
- **Solution**: Make sure Ollama is running (`ollama serve`)

**Issue**: Out of memory errors
- **Solution**: Reduce chunk size or process fewer documents at once

**Issue**: Slow embedding generation
- **Solution**: Consider using a GPU or smaller embedding model

---

## 📝 Development

### Running in Development Mode

```bash
streamlit run main.py --server.runOnSave true
```

### Adding New Features

1. Create new pages in `pages/` directory
2. Add utility functions in `utils/` directory
3. Update dependencies in `pyproject.toml`
4. Test thoroughly before committing

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.com/)
- Vector search by [ChromaDB](https://www.trychroma.com/)
- Embeddings from [Sentence Transformers](https://www.sbert.net/)
- AI models from [Google Gemini](https://deepmind.google/technologies/gemini/) and [Ollama](https://ollama.ai/)

---

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ and AI**
