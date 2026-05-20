import streamlit as st

def inject_style():
    theme = st.session_state.get("theme", "light")
    
    if theme == "light":
        theme_css = """
        :root {
            --gold: #C9A96E;
            --gold-light: #E8D5B0;
            --gold-dark: #8B6914;
            --bg: linear-gradient(135deg, #FAF7F2 0%, #EAE4D3 100%);
            --text: #000000;
            --text-muted: #3D3D3D;
            --card-bg: rgba(255, 255, 255, 0.9);
            --btn-text: #000000;
            --btn-bg: #FFFFFF;
            --border: rgba(201,169,110,0.4);
            --border-strong: rgba(201,169,110,0.6);
            --danger: #C0392B;
            --success: #27AE60;
            --hr: rgba(201,169,110,0.25);
            --hero-bg: linear-gradient(135deg, #FAF7F2 0%, #E8D5B0 100%);
            --hero-text: #000000;
        }
        """
    else:
        theme_css = """
        :root {
            --gold: #D4AF37;
            --gold-light: #F3E5AB;
            --gold-dark: #AA8822;
            --bg: #121212;
            --text: #FFFFFF;
            --text-muted: #B0B0B0;
            --card-bg: #1E1E1E;
            --btn-text: #FFFFFF;
            --btn-bg: #1E1E1E;
            --border: rgba(212,175,55,0.4);
            --border-strong: rgba(212,175,55,0.7);
            --danger: #CF6679;
            --success: #03DAC6;
            --hr: rgba(255,255,255,0.1);
            --hero-bg: linear-gradient(135deg, #121212 0%, #1E1E1E 100%);
            --hero-text: #FFFFFF;
        }
        """

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

        {{theme_css}}

        /* Base resets */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Jost', sans-serif;
            background: var(--bg) !important;
            color: var(--text) !important;
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: var(--bg) !important;
            border-right: 1px solid var(--border);
        }}
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {{
            color: var(--text) !important;
        }}

        /* Headers and Titles */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text) !important;
        }}

        /* Hide Streamlit default UI elements */
        [data-testid="stHeader"], [data-testid="stToolbar"], header {{ 
            display: none !important; 
        }}
        
        [data-testid="stSidebarNav"] {{ display: none !important; }}

        /* push content down */
        .main .block-container {{
            padding-top: 1rem !important;
            max-width: 1100px;
            background-color: transparent;
        }}

        /* Style for st.page_link */
        a[data-testid="stPageLink"] {{
            color: var(--btn-text) !important;
            text-decoration: none !important;
            text-transform: uppercase !important;
            letter-spacing: 0.2em !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            transition: all 0.3s !important;
            background-color: transparent !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
        }}
        a[data-testid="stPageLink"]:hover {{
            color: var(--text) !important;
        }}

        /* Input fields, selectboxes, and dropdowns */
        div[data-baseweb="input"], 
        div[data-baseweb="select"], 
        div[data-baseweb="popover"], 
        div[data-baseweb="menu"],
        div[role="listbox"],
        div[role="menu"],
        div[role="dialog"],
        .stTextInput input {{
            background-color: var(--card-bg) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            -webkit-text-fill-color: var(--text) !important;
        }}
        
        /* Show password button (eye icon) and other input-nested buttons */
        div[data-baseweb="input"] button {{
            background-color: transparent !important;
            border: none !important;
        }}
        
        div[data-baseweb="input"] button:hover {{
            background-color: rgba(255, 255, 255, 0.1) !important;
        }}
        
        /* Selectbox specific adjustments */
        div[data-baseweb="select"] > div {{
            background-color: var(--card-bg) !important;
            color: var(--text) !important;
        }}

        /* Radio buttons contrast */
        [data-testid="stMarkdownContainer"] p {{
            color: var(--text) !important;
        }}
        
        input, select, textarea, input[type="text"], input[type="password"], input[type="email"], input[type="tel"] {{
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
        }}
        ::placeholder {{
            color: var(--text-muted) !important;
            opacity: 0.7 !important;
        }}
        
        /* Tabs */
        button[data-baseweb="tab"] {{
            color: var(--text-muted) !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: var(--gold) !important;
            border-bottom-color: var(--gold) !important;
        }}

        /* Buttons - Global Override */
        button[data-testid^="baseButton"], button[kind="secondary"], button[kind="primary"], div.stButton > button, .stButton button, .stFormSubmitButton button {{
            border: 1px solid var(--border) !important;
            background-color: var(--btn-bg) !important;
            color: var(--btn-text) !important;
            font-weight: 800 !important;
            letter-spacing: 0.08em !important;
            transition: all 0.3s ease !important;
        }}
        button[data-testid^="baseButton"]:hover, button[kind="secondary"]:hover, button[kind="primary"]:hover, div.stButton > button:hover, .stButton button:hover, .stFormSubmitButton button:hover,
        button[data-testid^="baseButton"]:focus, button[data-testid^="baseButton"]:active {{
            border-color: var(--gold) !important;
            color: var(--gold) !important;
            box-shadow: 0 0 10px rgba(201,169,110,0.2) !important;
            background-color: var(--card-bg) !important;
        }}
        
        /* Theme Toggle specific - forcing opaque background in dark mode */
        .stButton button[data-testid="baseButton-secondary"] {{
            background-color: var(--card-bg) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
        }}

        /* Cards & Containers */
        .lum-card, [data-testid="stForm"] {{
            border: 1px solid var(--border) !important;
            padding: 1.5rem;
            background: var(--card-bg) !important;
            border-radius: 4px;
            color: var(--text) !important;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            color: var(--gold) !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: var(--text-muted) !important;
        }}
        
        /* Divider */
        hr {{
            border-top: 1px solid var(--hr) !important;
        }}

        /* Caption styling for better readability */
        [data-testid="stCaptionContainer"], .stCaption {{
            color: var(--text-muted) !important;
            font-size: 0.8rem !important;
            opacity: 1 !important;
        }}

        /* Success/Error message colors */
        .stAlert {{
            background-color: var(--card-bg) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
        }}

        /* Form Label Contrast */
        label[data-testid="stWidgetLabel"] p {{
            color: var(--text) !important;
            font-weight: 500 !important;
            letter-spacing: 0.02em !important;
        }}

        /* THE ULTIMATE CENTERING OVERRIDE - REVISED */
        .stPageLink, .stButton {{
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            text-align: center !important;
        }}
        
        .stPageLink > a, .stButton > button {{
            width: auto !important;
            min-width: 200px !important;
            margin: 0 auto !important;
        }}

        /* Prevent form buttons from being centered if not desired, 
           but for this app, centered forms look good too. 
           However, let's keep form buttons left-aligned if they are in a form. */
        [data-testid="stForm"] .stButton {{
            justify-content: flex-start !important;
        }}
        [data-testid="stForm"] .stButton > button {{
            margin: 0 !important;
            width: 100% !important;
        }}

        /* Table & DataFrame Styling - Forced Light-ish for compatibility */
        .stTable, [data-testid="stTable"], [data-testid="stDataFrame"] {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 4px !important;
        }}
        .stTable th {{
            background-color: #F0F2F6 !important;
            color: #000000 !important;
        }}
        .stTable td {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-bottom: 1px solid #E6E9EF !important;
        }}
        </style>
    """.replace("{theme_css}", theme_css), unsafe_allow_html=True)
