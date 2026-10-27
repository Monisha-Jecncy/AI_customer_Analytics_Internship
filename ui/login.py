"""
Premium split-panel login screen.
Left: branded showcase with animated orbs + feature highlights.
Right: sign-in form. Demo auth against config.DEMO_USERS.
"""
import streamlit as st
from config.settings import DEMO_USERS, AI_LABEL


def login_screen():
    # hide sidebar on the login screen for a full-focus experience
    st.markdown('<div class="login-hide-sidebar"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")

    # ---------- Left: brand showcase ----------
    with left:
        st.markdown(f"""
        <div class="login-brand">
            <div>
                <div class="lb-logo">🤖</div>
                <div class="lb-title">AI Customer<br>Analytics Platform</div>
                <div class="lb-sub">
                    Segment customers with K-Means, uncover insights with
                    Google Gemini AI, and turn raw data into marketing strategy —
                    all in one modern dashboard.
                </div>
                <div class="lb-feat"><span class="ic">📊</span> Automatic K-Means clustering</div>
                <div class="lb-feat"><span class="ic">🧠</span> Gemini AI insights &amp; chat</div>
                <div class="lb-feat"><span class="ic">📈</span> Interactive 2D &amp; 3D charts</div>
                <div class="lb-feat"><span class="ic">📄</span> One-click PDF &amp; Excel reports</div>
            </div>
            <div class="lb-foot">
                <span class="lb-pill">{AI_LABEL}</span>
                <span class="lb-pill">Scikit-learn</span>
                <span class="lb-pill">Plotly</span>
                <span class="lb-pill">Streamlit</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- Right: sign-in form ----------
    # Marker class lets the CSS style THIS column as the form card,
    # so Streamlit's own widgets sit inside it (no empty HTML wrapper box).
    with right:
        st.markdown('<div class="login-form-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-form-title">Welcome back 👋</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="login-form-sub">Sign in to access your dashboard</div>',
                    unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        remember = st.checkbox("Keep me signed in", value=True)

        if st.button("Sign In  →", use_container_width=True):
            if DEMO_USERS.get(username) == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials. Try admin / admin123")

        st.markdown(
            '<div class="login-demo">🔑 Demo login → '
            '<b>admin</b> / <b>admin123</b></div>',
            unsafe_allow_html=True)
