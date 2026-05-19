import streamlit as st

def inject_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

        :root {
            --gold: #C9A96E;
            --gold-light: #E8D5B0;
            --gold-dark: #8B6914;
            --bg: #FAF7F2;
            --text: #1A1A1A;
            --text-muted: #8A8476;
            --card-bg: #FFFFFF;
            --border: rgba(201,169,110,0.25);
            --border-strong: rgba(201,169,110,0.5);
            --danger: #C0392B;
            --success: #27AE60;
            --hr: rgba(201,169,110,0.15);
            --hero-bg: linear-gradient(135deg, #FAF7F2 0%, #E8D5B0 100%);
            --hero-text: #1A1A1A;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0E0B09;
                --text: #FAF7F2;
                --text-muted: #AFA99B;
                --card-bg: #1A1410;
                --border: rgba(201,169,110,0.15);
                --border-strong: rgba(201,169,110,0.3);
                --hr: rgba(201,169,110,0.1);
                --hero-bg: linear-gradient(135deg, #050403 0%, #1A1410 50%, #050403 100%);
                --hero-text: #FAF7F2;
            }
        }

        /* Base resets */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Jost', sans-serif;
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--bg) !important;
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            color: var(--text) !important;
        }

        /* Headers and Titles */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text) !important;
        }

        /* Hide Streamlit default UI elements */
        [data-testid="stHeader"], [data-testid="stToolbar"], header { 
            display: none !important; 
        }
        
        [data-testid="stSidebarNav"] { display: none !important; }

        /* push content down */
        .main .block-container {
            padding-top: 1rem !important;
            max-width: 1100px;
            background-color: transparent;
        }

        /* Style for st.page_link */
        a[data-testid="stPageLink"] {
            color: var(--text-muted) !important;
            text-decoration: none !important;
            text-transform: uppercase !important;
            letter-spacing: 0.15em !important;
            font-size: 0.75rem !important;
            transition: all 0.3s !important;
            background-color: transparent !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
        }
        a[data-testid="stPageLink"]:hover {
            color: var(--text) !important;
        }

        /* Input fields and selectboxes */
        div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="popover"] {
            background-color: var(--card-bg) !important;
        }
        input, select, textarea {
            color: var(--text) !important;
        }
        
        /* Tabs */
        button[data-baseweb="tab"] {
            color: var(--text-muted) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--gold) !important;
            border-bottom-color: var(--gold) !important;
        }

        /* Buttons */
        div.stButton > button {
            border: 1px solid var(--border);
            background-color: var(--card-bg);
            color: var(--text);
        }
        div.stButton > button:hover {
            border-color: var(--gold);
            color: var(--gold);
        }
        
        /* Cards & Containers */
        .lum-card {
            border: 1px solid var(--border);
            padding: 1.5rem;
            background: var(--card-bg);
            border-radius: 4px;
            color: var(--text);
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: var(--gold) !important;
        }
        [data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
        }
        
        /* Divider */
        hr {
            border-top: 1px solid var(--hr) !important;
        }
        </style>
    """, unsafe_allow_html=True)
