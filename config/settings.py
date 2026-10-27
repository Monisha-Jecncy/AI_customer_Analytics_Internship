"""
Central configuration for the AI Customer Analytics Platform.
Tweak these values to change app behaviour without touching core logic.
"""

# ---- App meta ----
APP_NAME = "AI Customer Analytics Platform"
APP_ICON = "🤖"
APP_VERSION = "1.0.0"

# ---- Auth (demo only — replace with a real auth backend in prod) ----
DEMO_USERS = {
    "admin": "admin123",
    "vino": "vino123",
}

# ---- Google Gemini API ----
# The API key is NEVER hard-coded. Provide it in ONE of these ways:
#   1) Environment variable:  GOOGLE_API_KEY=your_key
#   2) A .env file in the project root:  GOOGLE_API_KEY=your_key
#   3) .streamlit/secrets.toml:  GOOGLE_API_KEY = "your_key"
#   4) Paste it on the Settings page of the app (kept for the session only)
# Get a free key from https://aistudio.google.com/apikey
import os

GEMINI_MODEL = "gemini-3.5-flash"
# If the main model returns 404 (retired / not enabled for your key),
# the client automatically tries these in order.
GEMINI_FALLBACK_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-2.5-flash",
]
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_TIMEOUT = 120  # seconds
GEMINI_TEMPERATURE = 0.7


def _read_dotenv(key: str) -> str:
    """Tiny .env reader (no extra dependency)."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith(key + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def get_api_key() -> str:
    """Return the Google API key from session, env, .env or Streamlit secrets."""
    try:
        import streamlit as st
        if st.session_state.get("google_api_key"):
            return st.session_state["google_api_key"].strip()
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                return str(st.secrets["GOOGLE_API_KEY"]).strip()
        except Exception:
            pass
    except Exception:
        pass
    return (os.getenv("GOOGLE_API_KEY") or _read_dotenv("GOOGLE_API_KEY")).strip()


# Friendly label shown in the UI.
AI_LABEL = "Gemini"

# ---- Clustering ----
MAX_K = 10                        # upper bound for auto-K search
RANDOM_STATE = 42

# ---- Theme palette (used across Plotly + CSS) ----
PALETTE = [
    "#818cf8", "#a78bfa", "#ec4899", "#f43f5e", "#f59e0b",
    "#10b981", "#06b6d4", "#3b82f6", "#c084fc", "#2dd4bf",
]

# ---- Single premium dark theme (light removed) ----
THEME = {
    "bg": "#0a0e1a",
    "bg_alt": "#0f1629",
    "surface": "#141b2e",
    "surface_alt": "#1c2540",
    "text": "#f1f5f9",
    "text_muted": "#8b98b5",
    "primary": "#6366f1",
    "primary_glow": "#818cf8",
    "accent": "#ec4899",
    "accent2": "#06b6d4",
    "border": "rgba(129,140,248,0.18)",
    "plotly_template": "plotly_dark",
}
