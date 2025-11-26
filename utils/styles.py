import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* Main Container */
        .stApp {
            background-color: #0E1117;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #262730;
        }
        
        /* Titles */
        h1, h2, h3 {
            color: #FAFAFA !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Custom Card Style */
        .css-card {
            border-radius: 10px;
            padding: 20px;
            background-color: #1E1E1E;
            border: 1px solid #333;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Chat Messages */
        .stChatMessage {
            background-color: #1E1E1E;
            border-radius: 10px;
            border: 1px solid #333;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(45deg, #FF4B4B, #FF914D);
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
        }
        
        /* Inputs */
        .stTextInput > div > div > input {
            background-color: #262730;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #0E1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #333;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
    """, unsafe_allow_html=True)

def card(title, content):
    st.markdown(f"""
        <div class="css-card">
            <h3 style="margin-top: 0;">{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)
