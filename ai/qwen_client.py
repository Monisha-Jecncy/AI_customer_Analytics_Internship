"""
Gemini client — talks to the Google Gemini API using your Google API key.

Setup:
    1. Create a key at https://aistudio.google.com/apikey
    2. Set it as GOOGLE_API_KEY (environment variable, .env file,
       .streamlit/secrets.toml, or paste it on the Settings page).

This module is intentionally isolated so the model can be swapped by
editing config/settings.py only. (File/class names are kept as
qwen_client.py / QwenClient so the rest of the app needs no changes.)
"""

import time

import requests

from config.settings import (
    GEMINI_BASE_URL,
    GEMINI_MODEL,
    GEMINI_FALLBACK_MODELS,
    GEMINI_TIMEOUT,
    GEMINI_TEMPERATURE,
    get_api_key,
)


class QwenClient:
    """Thin wrapper around the Gemini generateContent endpoint."""

    def __init__(self, api_key: str | None = None, model: str = GEMINI_MODEL):
        self.api_key = (api_key or get_api_key()).strip()
        self.model = model
        self.base = GEMINI_BASE_URL.rstrip("/")

    def _headers(self) -> dict:
        return {"Content-Type": "application/json", "x-goog-api-key": self.api_key}

    def is_available(self) -> bool:
        """Check that a key is set and that the Gemini API accepts it."""
        if not self.api_key:
            return False
        try:
            r = requests.get(
                f"{self.base}/models/{self.model}", headers=self._headers(), timeout=10
            )
            return r.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, system: str | None = None) -> str:
        """Send a prompt to Gemini and return the text response."""
        if not self.api_key:
            return (
                "Google API key not found. Set GOOGLE_API_KEY or paste it "
                "on the Settings page."
            )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": GEMINI_TEMPERATURE},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        last = ""
        for model in [self.model] + [
            m for m in GEMINI_FALLBACK_MODELS if m != self.model
        ]:
            for attempt in range(3):  # retry busy-server errors
                try:
                    r = requests.post(
                        f"{self.base}/models/{model}:generateContent",
                        headers=self._headers(),
                        json=payload,
                        timeout=GEMINI_TIMEOUT,
                    )
                except requests.exceptions.ConnectionError:
                    return (
                        "Cannot reach the Gemini API. Check your "
                        "internet connection."
                    )
                except Exception as e:
                    return f"AI error: {e}"

                if r.status_code == 404:  # model retired / unavailable
                    last = f"Model '{model}' not found (404)."
                    break  # try next model
                if r.status_code in (500, 502, 503, 504):  # server busy
                    last = f"Model '{model}' is busy ({r.status_code})."
                    time.sleep(2 * (attempt + 1))
                    continue  # retry same model
                if r.status_code in (400, 401, 403):
                    msg = r.json().get("error", {}).get("message", r.text)
                    return f"API key / request error: {msg}"
                if r.status_code == 429:
                    return "Rate limit reached. Please wait a minute and " "try again."
                try:
                    r.raise_for_status()
                    data = r.json()
                    parts = data["candidates"][0]["content"]["parts"]
                    self.model = model  # remember the working model
                    return "".join(p.get("text", "") for p in parts).strip()
                except (KeyError, IndexError):
                    return (
                        "The model returned no text (the response may "
                        "have been blocked)."
                    )
                except Exception as e:
                    return f"AI error: {e}"
        return (
            f"{last} Gemini is busy or unavailable right now. "
            "Please click the button again in a few seconds."
        )


# ---------- High-level analytics helpers ----------

_SYSTEM = (
    "You are a senior customer analytics consultant. "
    "Be concise, data-driven, and practical. Use clear business language."
)


def customer_insights(client: QwenClient, profile_md: str) -> str:
    prompt = (
        "Given the following K-Means customer segment profiles, describe each "
        "segment's key characteristics and give it a memorable name.\n\n"
        f"{profile_md}"
    )
    return client.generate(prompt, system=_SYSTEM)


def marketing_strategy(client: QwenClient, profile_md: str) -> str:
    prompt = (
        "Based on these customer segments, propose a targeted marketing "
        "strategy per segment (channel, message, offer).\n\n"
        f"{profile_md}"
    )
    return client.generate(prompt, system=_SYSTEM)


def product_recommendations(client: QwenClient, profile_md: str) -> str:
    prompt = (
        "For each customer segment below, recommend product types or bundles "
        "most likely to convert, with a one-line rationale.\n\n"
        f"{profile_md}"
    )
    return client.generate(prompt, system=_SYSTEM)


def predict_segment(client: QwenClient, profile_md: str, customer: dict) -> str:
    prompt = (
        "Here are the existing segment profiles:\n"
        f"{profile_md}\n\n"
        "A new customer has these attributes:\n"
        f"{customer}\n\n"
        "Which segment do they most likely belong to and why? Suggest the "
        "next best action."
    )
    return client.generate(prompt, system=_SYSTEM)


def chat(client: QwenClient, question: str, context_md: str) -> str:
    prompt = (
        "You are answering questions about a clustered customer dataset.\n"
        f"Context (segment profiles):\n{context_md}\n\n"
        f"Question: {question}"
    )
    return client.generate(prompt, system=_SYSTEM)
