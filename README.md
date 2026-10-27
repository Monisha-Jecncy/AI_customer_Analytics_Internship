# 🤖 AI Customer Analytics Platform

Modern Streamlit dashboard for customer segmentation using **K-Means** +
**Google Gemini AI (via Google API key)**. Glass-morphism UI, dark/light themes,
2D/3D Plotly charts, AI insights, prediction, chat assistant, and PDF/Excel reports.

## 📁 Folder structure

```
ai_customer_analytics/
├── app.py                  # Entry point
├── requirements.txt
├── config/
│   └── settings.py         # App + theme + model config
├── core/
│   ├── data_processor.py   # Load + clean + scale
│   ├── clustering.py       # K-Means + auto-K
│   └── visualizer.py       # Plotly 2D/3D charts
├── ai/
│   └── qwen_client.py      # Gemini API client — SEPARATE model file
├── ui/
│   ├── styles.py           # Glass-morphism CSS
│   ├── login.py            # Login screen
│   └── dashboard.py        # Main dashboard tabs
├── reports/
│   └── exporter.py         # PDF + Excel export
├── utils/
├── assets/
└── data/
```

## ⚙️ Setup

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Google API key (get one: https://aistudio.google.com/apikey)
#    Windows (PowerShell):  $env:GOOGLE_API_KEY="your_key"
#    Mac/Linux:             export GOOGLE_API_KEY="your_key"
#    OR copy .env.example to .env and paste the key inside it
#    OR paste it on the app's Settings page
```

## ▶️ Run

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).

**Demo login:** `admin` / `admin123`

## 🧠 Swapping the AI model

All model config lives in `config/settings.py`:

```python
GEMINI_MODEL = "gemini-3.5-flash"   # see https://ai.google.dev/gemini-api/docs/models
```

The AI logic is fully isolated in `ai/qwen_client.py`. Never commit your API
key — keep it in `.env` / environment variables (already in `.gitignore`).

## ✨ Features

Login • Modern dashboard • Dark/Light theme • Dataset upload • Data cleaning •
Automatic K selection • K-Means • 2D & 3D charts • AI customer insights •
AI marketing strategy • AI product recommendation • Customer prediction •
AI chat assistant • PDF report • Excel report • Model comparison • Settings
