"""
Injects premium dark glass-morphism CSS into Streamlit.
Single dark theme — no light mode.
"""

import streamlit as st
from config.settings import THEME as t


def inject_css():
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* ---------- Animated gradient backdrop ---------- */
    .stApp {{
        background:
            radial-gradient(ellipse 80% 50% at 10% 0%, {t['primary']}26, transparent 55%),
            radial-gradient(ellipse 70% 60% at 95% 15%, {t['accent']}22, transparent 55%),
            radial-gradient(ellipse 60% 50% at 50% 100%, {t['accent2']}1c, transparent 55%),
            {t['bg']};
        color: {t['text']};
        font-family: 'Inter', sans-serif;
    }}
    .stApp::before {{
        content: ""; position: fixed; inset: 0; pointer-events: none;
        background-image:
            linear-gradient({t['border']} 1px, transparent 1px),
            linear-gradient(90deg, {t['border']} 1px, transparent 1px);
        background-size: 44px 44px;
        mask-image: radial-gradient(ellipse 60% 60% at 50% 40%, black, transparent 75%);
        opacity: 0.35; z-index: 0;
    }}

    #MainMenu, footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {{ visibility: hidden; }}
    /* keep the sidebar open/close arrow visible */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important; display: flex !important;
        color: #f1f5f9 !important; z-index: 999999;
    }}
    [data-testid="stSidebarCollapsedControl"] *,
    [data-testid="collapsedControl"] *,
    [data-testid="stExpandSidebarButton"] * {{ color: #f1f5f9 !important; }}
    .block-container {{ padding-top: 2rem; position: relative; z-index: 1; }}

    h1, h2, h3, h4 {{
        font-family: 'Space Grotesk', sans-serif;
        color: {t['text']}; font-weight: 700; letter-spacing: -0.02em;
    }}

    /* ---------- Gradient hero title ---------- */
    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.4rem; font-weight: 700; line-height: 1.1;
        background: linear-gradient(120deg, {t['primary_glow']}, {t['accent']} 55%, {t['accent2']});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-size: 200% auto; animation: shine 6s linear infinite;
    }}
    @keyframes shine {{ to {{ background-position: 200% center; }} }}

    /* ---------- Glass cards ---------- */
    .glass {{
        background: linear-gradient(160deg, {t['surface']}e6, {t['surface_alt']}cc);
        backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
        border: 1px solid {t['border']}; border-radius: 20px;
        padding: 1.5rem 1.7rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
        margin-bottom: 1rem;
    }}

    /* ---------- Metric tiles ---------- */
    .metric-card {{
        position: relative; overflow: hidden;
        background: linear-gradient(150deg, {t['surface']}f0, {t['surface_alt']}e0);
        border: 1px solid {t['border']}; border-radius: 18px;
        padding: 1.3rem 1rem; text-align: center;
        transition: transform .25s ease, box-shadow .25s ease;
    }}
    .metric-card::after {{
        content: ""; position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, {t['primary']}33, transparent 60%);
        opacity: 0; transition: opacity .3s ease;
    }}
    .metric-card:hover {{ transform: translateY(-4px);
        box-shadow: 0 16px 40px {t['primary']}44; }}
    .metric-card:hover::after {{ opacity: 1; }}
    .metric-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.1rem; font-weight: 700; position: relative; z-index: 1;
        background: linear-gradient(120deg, {t['primary_glow']}, {t['accent']});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .metric-label {{
        font-size: 0.72rem; color: {t['text_muted']}; position: relative; z-index: 1;
        text-transform: uppercase; letter-spacing: 0.08em; margin-top: .2rem;
    }}

    /* ---------- Buttons ---------- */
    .stButton > button {{
        background: linear-gradient(135deg, {t['primary']}, {t['accent']});
        color: white; border: none; border-radius: 13px;
        padding: 0.6rem 1.5rem; font-weight: 600; font-size: 0.9rem;
        box-shadow: 0 4px 18px {t['primary']}55;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px); filter: brightness(1.12);
        box-shadow: 0 10px 30px {t['primary']}77;
    }}
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {t['accent2']}, {t['primary']});
        color: white; border: none; border-radius: 13px; font-weight: 600;
        box-shadow: 0 4px 18px {t['accent2']}44;
    }}

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px; background: transparent; flex-wrap: wrap;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: {t['surface']}bb; border: 1px solid {t['border']};
        border-radius: 12px; padding: 9px 16px; color: {t['text_muted']};
        font-weight: 500; transition: all .2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: {t['text']}; border-color: {t['primary']}66; }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {t['primary']}, {t['accent']});
        color: white !important; border-color: transparent;
        box-shadow: 0 6px 20px {t['primary']}55;
    }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {t['surface']}f2, {t['bg_alt']}f2);
        backdrop-filter: blur(22px); border-right: 1px solid {t['border']};
    }}
    section[data-testid="stSidebar"] * {{ color: {t['text']}; }}

    /* ---------- Inputs ---------- */
    input, textarea, .stTextInput input, .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {{
        background: {t['surface']}cc !important;
        border: 1px solid {t['border']} !important;
        border-radius: 11px !important; color: {t['text']} !important;
    }}
    input:focus, textarea:focus {{ border-color: {t['primary']} !important;
        box-shadow: 0 0 0 3px {t['primary']}33 !important; }}

    /* ---------- Dataframe ---------- */
    .stDataFrame {{ border-radius: 14px; overflow: hidden;
        border: 1px solid {t['border']}; }}

    /* ---------- Badges ---------- */
    .badge {{
        display:inline-block; padding: 5px 14px; border-radius: 999px;
        background: linear-gradient(135deg, {t['primary']}2a, {t['accent']}2a);
        border: 1px solid {t['border']}; color: {t['primary_glow']};
        font-size: 0.75rem; font-weight: 600; margin: 3px 4px 3px 0;
    }}

    /* ---------- Nexchat-style Overview header ---------- */
    .ov-head {{ display:flex; align-items:center; justify-content:space-between;
        margin-bottom:1.4rem; }}
    .ov-title {{ font-family:'Space Grotesk',sans-serif; font-size:1.9rem;
        font-weight:700; color:{t['text']}; line-height:1.1; }}
    .ov-sub {{ color:{t['text_muted']}; font-size:0.9rem; margin-top:2px; }}
    .ov-avatar {{ width:46px; height:46px; border-radius:14px;
        background:linear-gradient(135deg,{t['primary']},{t['accent']});
        display:flex; align-items:center; justify-content:center; font-size:1.3rem;
        box-shadow:0 8px 24px {t['primary']}55; }}

    /* ---------- Hero gradient card (Messages & Leads equivalent) ---------- */
    .hero-card {{
        position:relative; overflow:hidden; border-radius:22px;
        padding:1.6rem 1.8rem 0.5rem; margin-bottom:1.3rem;
        background:
            radial-gradient(circle at 85% 15%, {t['accent']}44, transparent 45%),
            linear-gradient(135deg, {t['primary']}dd, {t['primary_glow']}aa 55%, {t['accent2']}88);
        border:1px solid {t['border']};
        box-shadow:0 16px 50px {t['primary']}44, inset 0 1px 0 rgba(255,255,255,0.12);
    }}
    .hero-card-title {{ font-family:'Space Grotesk',sans-serif; font-weight:600;
        font-size:1.15rem; color:#fff; }}
    .hero-card-tag {{ display:inline-block; padding:4px 12px; border-radius:999px;
        background:rgba(255,255,255,0.16); color:#fff; font-size:0.72rem;
        font-weight:600; }}

    /* ---------- Stat cards with trend badge ---------- */
    .stat-card {{
        position:relative; overflow:hidden;
        background:linear-gradient(155deg,{t['surface']}f2,{t['surface_alt']}dd);
        border:1px solid {t['border']}; border-radius:18px; padding:1.2rem 1.3rem;
        transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
    }}
    .stat-card:hover {{ transform:translateY(-4px);
        box-shadow:0 16px 40px {t['primary']}3a; border-color:{t['primary']}55; }}
    .stat-ic {{ width:40px; height:40px; border-radius:12px; font-size:1.1rem;
        display:flex; align-items:center; justify-content:center; margin-bottom:0.8rem;
        background:linear-gradient(135deg,{t['primary']}33,{t['accent']}33);
        border:1px solid {t['border']}; }}
    .stat-label {{ color:{t['text_muted']}; font-size:0.78rem; font-weight:500;
        text-transform:uppercase; letter-spacing:0.04em; }}
    .stat-row {{ display:flex; align-items:baseline; justify-content:space-between;
        margin-top:0.3rem; }}
    .stat-value {{ font-family:'Space Grotesk',sans-serif; font-size:1.7rem;
        font-weight:700; color:{t['text']}; }}
    .trend {{ font-size:0.75rem; font-weight:700; padding:3px 9px; border-radius:999px; }}
    .trend.up {{ color:#34d399; background:rgba(16,185,129,0.14); }}
    .trend.down {{ color:#fb7185; background:rgba(244,63,94,0.14); }}
    .trend.flat {{ color:{t['text_muted']}; background:{t['surface_alt']}; }}

    /* ---------- Section panel ---------- */
    .panel {{
        background:linear-gradient(160deg,{t['surface']}f0,{t['surface_alt']}d8);
        border:1px solid {t['border']}; border-radius:20px; padding:1.4rem 1.5rem;
        box-shadow:0 10px 34px rgba(0,0,0,0.32);
    }}
    .panel-head {{ display:flex; align-items:center; justify-content:space-between;
        margin-bottom:0.9rem; }}
    .panel-title {{ font-family:'Space Grotesk',sans-serif; font-weight:600;
        font-size:1.05rem; color:{t['text']}; }}

    /* ---------- Sidebar nav (radio styled as nav) ---------- */
    section[data-testid="stSidebar"] .stRadio > label {{ display:none; }}
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{ gap:4px; }}
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
        background:transparent; border-radius:12px; padding:10px 14px; margin:0;
        color:{t['text_muted']}; font-weight:500; font-size:0.92rem;
        transition:all .18s ease; cursor:pointer; border:1px solid transparent;
    }}
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {{
        background:{t['surface_alt']}aa; color:{t['text']}; }}
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {{
        background:linear-gradient(135deg,{t['primary']},{t['accent']});
        color:#fff; box-shadow:0 6px 18px {t['primary']}55; }}
    section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {{
        font-size:0.92rem; }}

    /* sidebar promo card */
    .promo {{
        margin-top:1.2rem; padding:1.2rem; border-radius:18px; text-align:center;
        background:linear-gradient(150deg,{t['primary']},{t['accent2']} 90%);
        box-shadow:0 12px 30px {t['primary']}44;
    }}
    .promo-emoji {{ font-size:2rem; }}
    .promo-title {{ font-family:'Space Grotesk',sans-serif; font-weight:700;
        color:#fff; margin-top:0.3rem; }}
    .promo-sub {{ color:rgba(255,255,255,0.85); font-size:0.76rem; margin-top:0.2rem; }}
    .sb-logo {{ font-family:'Space Grotesk',sans-serif; font-weight:700;
        font-size:1.25rem; display:flex; align-items:center; gap:8px;
        color:{t['text']}; margin-bottom:0.3rem; }}
    .sb-logo .x {{ width:30px;height:30px;border-radius:9px;
        background:linear-gradient(135deg,{t['primary']},{t['accent']});
        display:flex;align-items:center;justify-content:center;color:#fff; }}

    /* ---------- Premium Login ---------- */
    .login-hide-sidebar section[data-testid="stSidebar"] {{ display:none; }}

    .login-brand {{
        position: relative; overflow: hidden;
        min-height: 540px; border-radius: 26px; padding: 2.8rem 2.4rem;
        background:
            radial-gradient(circle at 20% 20%, {t['primary']}55, transparent 50%),
            radial-gradient(circle at 80% 80%, {t['accent']}44, transparent 50%),
            linear-gradient(150deg, {t['surface']}, {t['bg_alt']});
        border: 1px solid {t['border']};
        box-shadow: 0 30px 80px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.07);
        display: flex; flex-direction: column; justify-content: space-between;
    }}
    /* floating animated orbs */
    .login-brand::before, .login-brand::after {{
        content: ""; position: absolute; border-radius: 50%;
        filter: blur(50px); opacity: 0.55; z-index: 0;
    }}
    .login-brand::before {{
        width: 260px; height: 260px; top: -60px; right: -40px;
        background: {t['accent']}; animation: float1 9s ease-in-out infinite;
    }}
    .login-brand::after {{
        width: 220px; height: 220px; bottom: -50px; left: -30px;
        background: {t['primary_glow']}; animation: float2 11s ease-in-out infinite;
    }}
    @keyframes float1 {{ 0%,100%{{transform:translate(0,0)}} 50%{{transform:translate(-24px,30px)}} }}
    @keyframes float2 {{ 0%,100%{{transform:translate(0,0)}} 50%{{transform:translate(20px,-26px)}} }}

    .login-brand > * {{ position: relative; z-index: 1; }}
    .lb-logo {{
        display:inline-flex; align-items:center; justify-content:center;
        width:60px; height:60px; border-radius:18px; font-size:1.9rem;
        background: linear-gradient(135deg, {t['primary']}, {t['accent']});
        box-shadow: 0 10px 30px {t['primary']}66; margin-bottom: 1.2rem;
    }}
    .lb-title {{
        font-family:'Space Grotesk',sans-serif; font-size:2.3rem; font-weight:700;
        line-height:1.1; margin-bottom:0.7rem;
        background: linear-gradient(120deg, #fff, {t['primary_glow']} 60%, {t['accent']});
        background-size:200% auto; -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; animation: shine 6s linear infinite;
    }}
    .lb-sub {{ color:{t['text_muted']}; font-size:0.98rem; line-height:1.6;
        max-width:340px; margin-bottom:2rem; }}
    .lb-feat {{ display:flex; align-items:center; gap:12px; margin:0.7rem 0;
        color:{t['text']}; font-size:0.92rem; font-weight:500; }}
    .lb-feat span.ic {{
        display:inline-flex; align-items:center; justify-content:center;
        width:34px; height:34px; border-radius:10px; font-size:1rem;
        background:{t['primary']}22; border:1px solid {t['border']};
    }}
    .lb-foot {{ color:{t['text_muted']}; font-size:0.8rem; margin-top:2rem;
        display:flex; gap:8px; flex-wrap:wrap; }}
    .lb-pill {{ padding:4px 12px; border-radius:999px; background:{t['surface']}aa;
        border:1px solid {t['border']}; font-size:0.72rem; }}

    /* right form panel — styled via the column that holds the anchor marker,
       so Streamlit's real widgets live INSIDE the card (no empty box) */
    div[data-testid="column"]:has(.login-form-anchor) {{
        min-height: 540px; border-radius: 26px; padding: 2.4rem 2.2rem;
        background: linear-gradient(160deg, {t['surface']}f2, {t['surface_alt']}e6);
        border: 1px solid {t['border']};
        box-shadow: 0 30px 80px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.06);
        display: flex; flex-direction: column; justify-content: center;
    }}
    .login-form-anchor {{ height: 0; margin: 0; padding: 0; }}
    .login-form-title {{
        font-family:'Space Grotesk',sans-serif; font-size:1.7rem; font-weight:700;
        color:{t['text']}; margin-bottom:0.3rem;
    }}
    .login-form-sub {{ color:{t['text_muted']}; font-size:0.9rem; margin-bottom:1.6rem; }}
    .login-demo {{ text-align:center; color:{t['text_muted']}; font-size:0.78rem;
        margin-top:1.2rem; padding:0.6rem; border-radius:10px;
        background:{t['primary']}12; border:1px dashed {t['border']}; }}

    /* ---------- Alerts / chat ---------- */
    .stChatMessage {{ background: {t['surface']}bb; border: 1px solid {t['border']};
        border-radius: 14px; }}
    .stAlert {{ border-radius: 13px; }}

    /* scrollbar */
    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: {t['bg']}; }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient({t['primary']}, {t['accent']});
        border-radius: 6px; }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def metric(label: str, value):
    st.markdown(
        f'<div class="metric-card"><div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def glass(content_md: str):
    st.markdown(f'<div class="glass">{content_md}</div>', unsafe_allow_html=True)


def stat_card(
    icon: str, label: str, value, trend_text: str = "", trend_dir: str = "flat"
):
    """Nexchat-style stat card with an icon and a trend badge."""
    arrow = {"up": "▲", "down": "▼", "flat": "•"}.get(trend_dir, "•")
    badge = (
        f'<span class="trend {trend_dir}">{arrow} {trend_text}</span>'
        if trend_text
        else ""
    )
    st.markdown(
        f'<div class="stat-card"><div class="stat-ic">{icon}</div>'
        f'<div class="stat-label">{label}</div>'
        f'<div class="stat-row"><span class="stat-value">{value}</span>{badge}</div></div>',
        unsafe_allow_html=True,
    )


def overview_header(title: str, subtitle: str, avatar: str = "🧑‍💻"):
    st.markdown(
        f'<div class="ov-head"><div><div class="ov-title">{title}</div>'
        f'<div class="ov-sub">{subtitle}</div></div>'
        f'<div class="ov-avatar">{avatar}</div></div>',
        unsafe_allow_html=True,
    )


def panel_open(title: str, right: str = ""):
    st.markdown(
        f'<div class="panel"><div class="panel-head">'
        f'<div class="panel-title">{title}</div>'
        f'<div style="color:#8b98b5;font-size:0.8rem">{right}</div></div>',
        unsafe_allow_html=True,
    )


def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)
