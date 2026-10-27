"""
AI Customer Analytics Platform — entry point.
Nexchat-style sidebar nav + premium dark dashboard.

Run with:  streamlit run app.py
"""
import streamlit as st

from config.settings import APP_NAME, APP_ICON, APP_VERSION, AI_LABEL
from ui.styles import inject_css
from ui.login import login_screen
from ui.dashboard import render_page

st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON,
                   layout="wide", initial_sidebar_state="expanded")

st.session_state.setdefault("authenticated", False)

inject_css()

# ---- Login gate ----
if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ---- Sidebar: Nexchat-style nav ----
NAV = {
    "Overview": "🏠",
    "AI Agents": "🤖",
    "Clustering": "📊",
    "Charts": "📈",
    "AI Insights": "🧠",
    "Prediction": "🎯",
    "Chat": "💬",
    "Reports": "📄",
    "Compare": "⚖️",
    "Settings": "⚙️",
}

with st.sidebar:
    st.markdown(
        '<div class="sb-logo"><span class="x">X</span> Nexlytics</div>',
        unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#8b98b5;font-size:0.78rem;margin:-4px 0 1rem 2px">'
        'AI Customer Analytics</p>', unsafe_allow_html=True)

    choice = st.radio(
        "nav",
        list(NAV.keys()),
        format_func=lambda k: f"{NAV[k]}   {k}",
        label_visibility="collapsed",
    )

    st.markdown("""
        <div class="promo">
            <div class="promo-emoji">💬</div>
            <div class="promo-title">Quick Onboarding</div>
            <div class="promo-sub">Upload a dataset and run your first
            segmentation in under a minute.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"👤 **{st.session_state.get('username','user')}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.caption(f"v{APP_VERSION} • Google {AI_LABEL} API")

# ---- Route to selected page ----
render_page(choice)
