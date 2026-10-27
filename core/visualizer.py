"""
Plotly charts — elbow, silhouette, 2D and 3D cluster scatter, cluster sizes.
Styled for the premium dark theme (transparent bg, glow palette).
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from config.settings import PALETTE

# transparent layout so charts blend into the glass cards
_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c7d0e6", family="Inter"),
    title_font=dict(family="Space Grotesk", size=17, color="#f1f5f9"),
    margin=dict(l=20, r=20, t=50, b=20),
)


def _apply(fig, height):
    fig.update_layout(height=height, **_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(129,140,248,0.12)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(129,140,248,0.12)", zeroline=False)
    return fig


def elbow_chart(ks, inertias, template):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ks, y=inertias, mode="lines+markers",
        line=dict(color=PALETTE[0], width=3, shape="spline"),
        marker=dict(size=10, color=PALETTE[2],
                    line=dict(width=2, color="rgba(255,255,255,0.5)")),
        fill="tozeroy", fillcolor="rgba(129,140,248,0.08)",
    ))
    fig.update_layout(title="Elbow Method (Inertia vs K)",
                      xaxis_title="Clusters (K)", yaxis_title="Inertia",
                      template=template)
    return _apply(fig, 380)


def silhouette_chart(ks, scores, template):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ks, y=scores,
        marker=dict(color=[PALETTE[i % len(PALETTE)] for i in range(len(ks))],
                    line=dict(width=0)),
    ))
    fig.update_layout(title="Silhouette Score by K",
                      xaxis_title="Clusters (K)", yaxis_title="Silhouette",
                      template=template)
    return _apply(fig, 380)


def scatter_2d(df, x, y, labels, template):
    d = df.copy()
    d["Cluster"] = [f"Cluster {c}" for c in labels]
    fig = px.scatter(d, x=x, y=y, color="Cluster",
                     color_discrete_sequence=PALETTE, opacity=0.85)
    fig.update_traces(marker=dict(size=10,
                      line=dict(width=0.6, color="rgba(255,255,255,0.4)")))
    fig.update_layout(title=f"2D Clusters — {x} vs {y}", template=template)
    return _apply(fig, 460)


def scatter_3d(df, x, y, z, labels, template):
    d = df.copy()
    d["Cluster"] = [f"Cluster {c}" for c in labels]
    fig = px.scatter_3d(d, x=x, y=y, z=z, color="Cluster",
                        color_discrete_sequence=PALETTE, opacity=0.85)
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(title=f"3D Clusters — {x}, {y}, {z}", template=template,
                      height=560, **_LAYOUT)
    fig.update_scenes(xaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
                      yaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
                      zaxis=dict(backgroundcolor="rgba(0,0,0,0)"))
    return fig


def cluster_sizes(profile: pd.DataFrame, template):
    fig = px.bar(profile, x="Cluster", y="Size", text="Percent",
                 color="Cluster", color_discrete_sequence=PALETTE)
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(title="Segment Sizes", template=template, showlegend=False)
    return _apply(fig, 380)
