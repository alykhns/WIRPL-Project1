import streamlit as st

def inject_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

        :root {
            --gold: #C9A96E;
            --gold-light: #E8D5B0;
            --gold-dark: #8B6914;
            --cream: #FAF7F2;
            --charcoal: #1A1A1A;
            --charcoal-mid: #2D2D2D;
            --muted: #8A8476;
            --border: rgba(201,169,110,0.25);
            --border-strong: rgba(201,169,110,0.5);
            --danger: #C0392B;
            --success: #27AE60;
        }

        html, body, [class*="css"] {
            font-family: 'Jost', sans-serif;
            background-color: #FAF7F2;
            color: #1A1A1A;
        }

        /* hide sidebar & hamburger */
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        header { display: none !important; }

        /* push content down so navbar doesn't overlap */
        .main .block-container {
            padding-top: 5rem !important;
            max-width: 1100px;
        }

        /* navbar */
        .lum-nav {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 9999;
            height: 64px;
            background: rgba(250,247,242,0.96);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(201,169,110,0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2.5rem;
        }
        .lum-nav-logo {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.7rem;
            font-weight: 400;
            letter-spacing: 0.08em;
            color: #1A1A1A;
            text-decoration: none;
        }
        .lum-nav-logo em { color: #C9A96E; font-style: italic; }

        .lum-nav-links {
            display: flex;
            gap: 2.2rem;
            list-style: none;
            margin: 0; padding: 0;
        }
        .lum-nav-links a {
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #8A8476;
            text-decoration: none;
            transition: color 0.2s;
        }
        .lum-nav-links a:hover { color: #1A1A1A; }

        .lum-nav-cart {
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #8A8476;
            text-decoration: none;
            border: 1px solid rgba(201,169,110,0.4);
            padding: 6px 16px;
            transition: all 0.2s;
        }
        .lum-nav-cart:hover {
            background: #C9A96E;
            color: white;
            border-color: #C9A96E;
        }
        </style>

        <nav class="lum-nav">
            <a class="lum-nav-logo" href="/">Lumi<em>è</em>re</a>
            <ul class="lum-nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/Katalog">Katalog</a></li>
                <li><a href="/Detail_Produk">Detail Produk</a></li>
                <li><a href="/Riwayat">Riwayat</a></li>
            </ul>
            <a class="lum-nav-cart" href="/Cart">◇ &nbsp;Cart</a>
        </nav>
    """, unsafe_allow_html=True)