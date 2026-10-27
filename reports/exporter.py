"""
Report exporters — PDF (reportlab) and Excel (openpyxl via pandas).
"""
import io
from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
)

from config.settings import APP_NAME


def build_pdf(profile: pd.DataFrame, insights: str, strategy: str) -> bytes:
    """Return a PDF report as bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("t", parent=styles["Title"],
                           textColor=colors.HexColor("#6366f1"))
    h2 = ParagraphStyle("h2", parent=styles["Heading2"],
                        textColor=colors.HexColor("#334155"))

    story = [
        Paragraph(APP_NAME, title),
        Paragraph(f"Generated: {datetime.now():%Y-%m-%d %H:%M}", styles["Normal"]),
        Spacer(1, 0.6 * cm),
        Paragraph("Segment Profiles", h2),
    ]

    data = [list(profile.columns)] + profile.astype(str).values.tolist()
    tbl = Table(data, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366f1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f1f5f9")]),
    ]))
    story += [tbl, Spacer(1, 0.6 * cm)]

    story += [Paragraph("AI Customer Insights", h2),
              Paragraph(insights.replace("\n", "<br/>"), styles["Normal"]),
              Spacer(1, 0.5 * cm),
              Paragraph("AI Marketing Strategy", h2),
              Paragraph(strategy.replace("\n", "<br/>"), styles["Normal"])]

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def build_excel(df: pd.DataFrame, profile: pd.DataFrame) -> bytes:
    """Return an Excel workbook (clustered data + profiles) as bytes."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xl:
        df.to_excel(xl, sheet_name="Clustered Data", index=False)
        profile.to_excel(xl, sheet_name="Segment Profiles", index=False)
    buf.seek(0)
    return buf.getvalue()
