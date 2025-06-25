import streamlit as st

def load_css():
    """
    Load custom CSS styles for Streamlit
    """
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Sidebar */
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        
        /* Headers */
        h1 {
            color: #1E88E5;
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
        }
        
        h2 {
            color: #1976D2;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            color: #1565C0;
            font-size: 1.5rem;
            margin-bottom: 0.75rem;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            margin: 0.25rem 0;
            background-color: #1E88E5;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #1976D2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Text inputs */
        .stTextInput>div>div>input {
            border-radius: 4px;
            border: 1px solid #E0E0E0;
            padding: 0.5rem;
        }
        
        /* Select boxes */
        .stSelectbox>div>div>select {
            border-radius: 4px;
            border: 1px solid #E0E0E0;
            padding: 0.5rem;
        }
        
        /* Chat messages */
        .user-message {
            background-color: #E3F2FD;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        .assistant-message {
            background-color: #F5F5F5;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Code blocks */
        .stCodeBlock {
            background-color: #263238;
            color: #FFFFFF;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        /* Tables */
        .stTable {
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }
        
        .stTable th {
            background-color: #1E88E5;
            color: white;
            padding: 0.75rem;
            text-align: left;
        }
        
        .stTable td {
            padding: 0.75rem;
            border: 1px solid #E0E0E0;
        }
        
        /* Alerts */
        .stAlert {
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .stSuccess {
            background-color: #C8E6C9;
            color: #2E7D32;
        }
        
        .stError {
            background-color: #FFCDD2;
            color: #C62828;
        }
        
        .stWarning {
            background-color: #FFF9C4;
            color: #F9A825;
        }
        
        .stInfo {
            background-color: #E3F2FD;
            color: #1565C0;
        }
        
        /* Progress bars */
        .stProgress>div>div>div {
            background-color: #1E88E5;
        }
        
        /* Tooltips */
        .stTooltip {
            position: relative;
            display: inline-block;
        }
        
        .stTooltip .tooltiptext {
            visibility: hidden;
            background-color: #263238;
            color: white;
            text-align: center;
            padding: 0.5rem;
            border-radius: 4px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .stTooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        /* Tabs */
        .stTabs {
            margin-top: 1rem;
        }
        
        .stTab {
            padding: 0.5rem 1rem;
            margin-right: 0.25rem;
            border-radius: 4px 4px 0 0;
            border: 1px solid #E0E0E0;
            border-bottom: none;
            background-color: white;
            cursor: pointer;
        }
        
        .stTab[aria-selected="true"] {
            background-color: #1E88E5;
            color: white;
            border-color: #1E88E5;
        }
        
        /* File uploader */
        .stFileUploader {
            border: 2px dashed #E0E0E0;
            border-radius: 4px;
            padding: 1rem;
            text-align: center;
            margin: 1rem 0;
        }
        
        .stFileUploader:hover {
            border-color: #1E88E5;
        }
        
        /* Markdown */
        .stMarkdown {
            line-height: 1.6;
        }
        
        .stMarkdown a {
            color: #1E88E5;
            text-decoration: none;
        }
        
        .stMarkdown a:hover {
            text-decoration: underline;
        }
        
        /* Custom classes */
        .centered {
            text-align: center;
        }
        
        .flex-container {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .card {
            background-color: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        .badge {
            background-color: #1E88E5;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 999px;
            font-size: 0.875rem;
        }
        </style>
    """, unsafe_allow_html=True) 