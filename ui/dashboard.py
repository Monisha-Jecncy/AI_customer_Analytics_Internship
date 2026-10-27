"""
Dashboard pages — Nexchat-style layout, premium dark theme.
render_page(name) routes the sidebar nav choice to the matching page.
"""
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score

from config.settings import THEME, AI_LABEL, GEMINI_MODEL, get_api_key
from core import data_processor as dp
from core import clustering as cl
from core import visualizer as viz
from ai import qwen_client as qc
from reports import exporter as ex
from core import chart_export as ce
from ui.styles import (stat_card, overview_header, panel_open, panel_close, metric)

TMPL = THEME["plotly_template"]


def _profile_md(profile: pd.DataFrame) -> str:
    return profile.to_markdown(index=False)


def _need_clusters() -> bool:
    if "labels" not in st.session_state:
        st.info("Run a clustering job first from the **Clustering** page. 📊")
        return False
    return True


# ============================================================ OVERVIEW
def page_overview():
    ss = st.session_state
    overview_header("Overview",
                    f"Welcome back, {ss.get('username','there')} 👋 "
                    "Here's your segmentation snapshot.")

    has = "profile" in ss
    n_rows = len(ss.df) if "df" in ss else 0
    n_clusters = len(set(ss.labels)) if "labels" in ss else 0
    n_feats = len(ss.feats) if "feats" in ss else 0
    sil = ss.k_search["best_silhouette"] if "k_search" in ss else None

    # ---- Hero card ----
    st.markdown(
        '<div class="hero-card"><div style="display:flex;justify-content:space-between;'
        'align-items:center;margin-bottom:0.4rem">'
        '<span class="hero-card-title">Customer Segmentation Overview</span>'
        f'<span class="hero-card-tag">K-Means • {AI_LABEL}</span></div>',
        unsafe_allow_html=True)
    if has:
        st.plotly_chart(viz.cluster_sizes(ss.profile, TMPL),
                        use_container_width=True)
    else:
        st.markdown(
            '<p style="color:rgba(255,255,255,0.85);padding:1.5rem 0">'
            'No segments yet — upload a dataset and run clustering to light this up. ✨</p>',
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Stat cards row ----
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("👥", "Customers", f"{n_rows:,}",
                  "loaded" if n_rows else "", "up" if n_rows else "flat")
    with c2:
        stat_card("🧩", "Segments", n_clusters or "—",
                  "auto-K" if n_clusters else "", "up" if n_clusters else "flat")
    with c3:
        stat_card("📐", "Features", n_feats or "—",
                  "in model" if n_feats else "", "flat")
    with c4:
        stat_card("✨", "Silhouette", f"{sil:.2f}" if sil else "—",
                  "quality" if sil else "", "up" if sil else "flat")

    st.write("")

    # ---- Two lower panels ----
    left, right = st.columns([1.2, 1], gap="medium")
    with left:
        panel_open("Segment Profiles", "K-Means")
        if has:
            st.dataframe(ss.profile, use_container_width=True, height=260)
        else:
            st.caption("Segment averages will appear here after clustering.")
        panel_close()
    with right:
        panel_open("AI Snapshot", AI_LABEL)
        if ss.get("ai_insights"):
            st.markdown(ss["ai_insights"][:600] + "…")
        else:
            st.caption("Generate insights on the AI Insights page to see a "
                       "summary of your segments here. 🧠")
        panel_close()


# ============================================================ AI AGENTS (upload)
def page_upload():
    ss = st.session_state
    overview_header("Data & Agents", "Upload a dataset and let the AI clean it.")
    panel_open("Dataset Upload & Cleaning")
    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    if file:
        df = dp.load_dataset(file)
        clean, report = dp.clean_data(df)
        ss.df = clean
        ss.numeric_features = report["numeric_features"]
        st.write("")
        c1, c2, c3, c4 = st.columns(4)
        with c1: stat_card("📋", "Rows", f"{report['final_rows']:,}")
        with c2: stat_card("🧮", "Columns", report["final_cols"])
        with c3: stat_card("🧹", "Duplicates", report["duplicates_removed"], "removed", "down")
        with c4: stat_card("🩹", "Filled", report["values_filled"], "cleaned", "up")
        st.write("")
        st.dataframe(clean.head(20), use_container_width=True)
    panel_close()


# ============================================================ CLUSTERING
def page_clustering():
    ss = st.session_state
    overview_header("Clustering", "Group customers with K-Means.")
    if "df" not in ss:
        st.info("Upload a dataset first from the **AI Agents** page. 📤")
        return
    panel_open("K-Means Configuration")
    feats = st.multiselect("Numeric features", ss.numeric_features,
                           default=ss.numeric_features[:min(3, len(ss.numeric_features))])
    auto = st.checkbox("Automatic K selection", value=True)
    k = 4 if auto else st.slider("K (clusters)", 2, 10, 4)
    if st.button("🚀 Run Clustering") and feats:
        X = dp.scale_features(ss.df, feats)
        if auto:
            res = cl.auto_select_k(X); k = res["best_k"]; ss.k_search = res
            st.success(f"Auto-selected K = {k} "
                       f"(silhouette {res['best_silhouette']:.3f}) ✅")
        labels, _ = cl.run_kmeans(X, k)
        ss.labels, ss.feats = labels, feats
        ss.df["Cluster"] = labels
        ss.profile = cl.profile_clusters(ss.df, feats, labels)
    panel_close()
    if "profile" in ss:
        st.write("")
        panel_open("Segment Profiles")
        st.dataframe(ss.profile, use_container_width=True)
        panel_close()


# ============================================================ CHARTS
def _download_png(fig, filename: str, key: str):
    """Render a per-chart PNG download button (falls back silently)."""
    png = ce.fig_to_png(fig)
    if png:
        st.download_button("⬇️ PNG", png, f"{filename}.png", "image/png",
                           key=key, use_container_width=True)
    else:
        st.caption("Use the 📷 icon on the chart to save.")


def page_charts():
    ss = st.session_state
    overview_header("Charts", "Explore your clusters visually.")
    if not _need_clusters():
        return

    feats = ss.feats
    figs = {}  # collected for the "download all" ZIP

    # build all figures up front so we can also zip them
    if "k_search" in ss:
        r = ss.k_search
        figs["elbow"] = viz.elbow_chart(r["ks"], r["inertias"], TMPL)
        figs["silhouette"] = viz.silhouette_chart(r["ks"], r["silhouettes"], TMPL)
    figs["cluster_sizes"] = viz.cluster_sizes(ss.profile, TMPL)
    if len(feats) >= 2:
        ss.setdefault("_2d_axes", (feats[0], feats[1]))

    # ---- Elbow + Silhouette ----
    if "k_search" in ss:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(figs["elbow"], use_container_width=True)
            _download_png(figs["elbow"], "elbow_method", "dl_elbow")
        with c2:
            st.plotly_chart(figs["silhouette"], use_container_width=True)
            _download_png(figs["silhouette"], "silhouette_scores", "dl_sil")

    # ---- Cluster sizes ----
    st.plotly_chart(figs["cluster_sizes"], use_container_width=True)
    _download_png(figs["cluster_sizes"], "segment_sizes", "dl_sizes")

    # ---- 2D scatter (axis selectable) ----
    if len(feats) >= 2:
        c1, c2 = st.columns(2)
        x = c1.selectbox("X axis", feats, 0)
        y = c2.selectbox("Y axis", feats, 1)
        fig2d = viz.scatter_2d(ss.df, x, y, ss.labels, TMPL)
        figs["scatter_2d"] = fig2d
        st.plotly_chart(fig2d, use_container_width=True)
        _download_png(fig2d, f"clusters_2d_{x}_{y}", "dl_2d")

    # ---- 3D scatter ----
    if len(feats) >= 3:
        fig3d = viz.scatter_3d(ss.df, feats[0], feats[1], feats[2], ss.labels, TMPL)
        figs["scatter_3d"] = fig3d
        st.plotly_chart(fig3d, use_container_width=True)
        _download_png(fig3d, "clusters_3d", "dl_3d")

    # ---- Download ALL charts as ZIP (now that every fig exists) ----
    st.write("")
    panel_open("Export", "All charts")
    zip_bytes = ce.charts_to_zip(figs)
    if zip_bytes:
        st.download_button("⬇️ Download all charts (ZIP)", zip_bytes,
                           "all_charts.zip", "application/zip",
                           key="dl_all_zip", use_container_width=True)
    else:
        st.caption("PNG export unavailable — use each chart's 📷 icon instead.")
    panel_close()


# ============================================================ AI INSIGHTS
def page_insights():
    ss = st.session_state
    overview_header("AI Insights", f"Powered by Google {AI_LABEL}.")
    client = qc.QwenClient()
    if not client.is_available():
        if not get_api_key():
            st.warning("⚠️ Google API key not found. Add GOOGLE_API_KEY "
                       "(see README) or paste it on the **Settings** page.")
        else:
            st.warning(f"⚠️ Could not reach Gemini model '{GEMINI_MODEL}'. "
                       "Check your API key and internet connection.")
    if "profile" not in ss:
        st.info("Run clustering first. 🧠")
        return
    pmd = _profile_md(ss.profile)
    c1, c2, c3 = st.columns(3)
    if c1.button("✨ Customer Insights"):
        with st.spinner(f"{AI_LABEL} is thinking..."):
            ss.ai_insights = qc.customer_insights(client, pmd)
    if c2.button("📣 Marketing Strategy"):
        with st.spinner(f"{AI_LABEL} is thinking..."):
            ss.ai_strategy = qc.marketing_strategy(client, pmd)
    if c3.button("🛍️ Product Recommendations"):
        with st.spinner(f"{AI_LABEL} is thinking..."):
            ss.ai_products = qc.product_recommendations(client, pmd)
    for key, title in [("ai_insights", "Customer Insights"),
                       ("ai_strategy", "Marketing Strategy"),
                       ("ai_products", "Product Recommendations")]:
        if key in ss:
            st.write("")
            panel_open(title, AI_LABEL)
            st.markdown(ss[key])
            panel_close()


# ============================================================ PREDICTION
def page_prediction():
    ss = st.session_state
    overview_header("Prediction", "Assign a new customer to a segment.")
    if "profile" not in ss:
        st.info("Run clustering first. 🎯")
        return
    panel_open("New Customer")
    inputs = {}
    cols = st.columns(min(3, len(ss.feats)))
    for i, f in enumerate(ss.feats):
        inputs[f] = cols[i % len(cols)].number_input(f, value=float(ss.df[f].mean()))
    go = st.button("🎯 Predict Segment")
    panel_close()
    if go:
        client = qc.QwenClient()
        with st.spinner("Predicting..."):
            out = qc.predict_segment(client, _profile_md(ss.profile), inputs)
        st.write("")
        panel_open("Prediction", AI_LABEL)
        st.markdown(out)
        panel_close()


# ============================================================ CHAT
def page_chat():
    ss = st.session_state
    overview_header("AI Chat Assistant", "Ask anything about your segments.")
    if "profile" not in ss:
        st.info("Run clustering first. 💬")
        return
    ss.setdefault("chat_history", [])
    for role, msg in ss.chat_history:
        with st.chat_message(role):
            st.markdown(msg)
    q = st.chat_input("Ask about your customer segments...")
    if q:
        ss.chat_history.append(("user", q))
        client = qc.QwenClient()
        with st.spinner("Thinking..."):
            ans = qc.chat(client, q, _profile_md(ss.profile))
        ss.chat_history.append(("assistant", ans))
        st.rerun()


# ============================================================ REPORTS
def page_reports():
    ss = st.session_state
    overview_header("Reports", "Export your analysis.")
    if "profile" not in ss:
        st.info("Run clustering first. 📄")
        return
    panel_open("Download")
    c1, c2 = st.columns(2)
    pdf = ex.build_pdf(ss.profile, ss.get("ai_insights", "Not generated yet."),
                       ss.get("ai_strategy", "Not generated yet."))
    c1.download_button("⬇️ PDF Report", pdf, "customer_report.pdf",
                       "application/pdf", use_container_width=True)
    xlsx = ex.build_excel(ss.df, ss.profile)
    c2.download_button("⬇️ Excel Report", xlsx, "customer_report.xlsx",
                       "application/vnd.openxmlformats-officedocument."
                       "spreadsheetml.sheet", use_container_width=True)
    panel_close()


# ============================================================ COMPARE
def page_compare():
    ss = st.session_state
    overview_header("Model Comparison", "K-Means vs Agglomerative.")
    if "feats" not in ss:
        st.info("Run clustering first. ⚖️")
        return
    X = dp.scale_features(ss.df, ss.feats)
    k = len(set(ss.labels))
    rows = []
    for name, model in [("K-Means", KMeans(n_clusters=k, random_state=42, n_init=10)),
                        ("Agglomerative", AgglomerativeClustering(n_clusters=k))]:
        lbl = model.fit_predict(X)
        rows.append({"Model": name, "K": k,
                     "Silhouette": round(silhouette_score(X, lbl), 3)})
    panel_open("Results")
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    panel_close()


# ============================================================ SETTINGS
def page_settings():
    ss = st.session_state
    overview_header("Settings", "Session & model configuration.")
    panel_open("Configuration")
    st.write(f"**User:** {ss.get('username', 'guest')}")
    st.write("**Theme:** Premium Dark")
    st.write(f"**Model:** {GEMINI_MODEL} (Google Gemini API)")
    key_in = st.text_input("Google API key", type="password",
                           value=ss.get("google_api_key", ""),
                           placeholder="Paste your key (session only)")
    if key_in != ss.get("google_api_key", ""):
        ss["google_api_key"] = key_in
        st.success("API key saved for this session. ✅")
    st.caption("Status: " + ("🟢 key detected" if get_api_key() else "🔴 no key"))
    if st.button("🧹 Clear session data"):
        for k in ["df", "labels", "profile", "feats", "k_search",
                  "chat_history", "ai_insights", "ai_strategy", "ai_products"]:
            ss.pop(k, None)
        st.success("Session cleared. ✅")
    panel_close()


# ============================================================ ROUTER
_PAGES = {
    "Overview": page_overview,
    "AI Agents": page_upload,
    "Clustering": page_clustering,
    "Charts": page_charts,
    "AI Insights": page_insights,
    "Prediction": page_prediction,
    "Chat": page_chat,
    "Reports": page_reports,
    "Compare": page_compare,
    "Settings": page_settings,
}


def render_page(name: str):
    _PAGES.get(name, page_overview)()
