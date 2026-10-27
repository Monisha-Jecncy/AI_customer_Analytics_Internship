"""
Chart export helpers — turn Plotly figures into downloadable PNGs,
and bundle multiple charts into a single ZIP.

Uses kaleido 0.2.1 (no Chrome dependency). If export ever fails,
functions return None so the UI can fall back gracefully to the
built-in Plotly camera icon.
"""
import io
import zipfile


def fig_to_png(fig, width: int = 1000, height: int = 560, scale: int = 2):
    """Render a Plotly figure to PNG bytes. Returns None on failure."""
    try:
        return fig.to_image(format="png", width=width, height=height, scale=scale)
    except Exception:
        return None


def charts_to_zip(named_figs: dict) -> bytes | None:
    """
    Bundle {filename: figure} into a ZIP of PNGs.
    Returns ZIP bytes, or None if nothing could be exported.
    """
    buf = io.BytesIO()
    wrote = 0
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, fig in named_figs.items():
            png = fig_to_png(fig)
            if png:
                zf.writestr(f"{name}.png", png)
                wrote += 1
    if not wrote:
        return None
    buf.seek(0)
    return buf.getvalue()
