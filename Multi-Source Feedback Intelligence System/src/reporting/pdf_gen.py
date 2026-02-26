import os
from datetime import datetime, timezone, timedelta
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

from src.database import SessionLocal
from src.analytics.queries import (
    get_kpis,
    get_sentiment_timeseries,
    get_trend_status,
    get_top_categories,
    get_high_priority_feedback,
)
from src.intelligence.ai_summary import generate_ai_summary


REPORTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "reports")
)

os.makedirs(REPORTS_DIR, exist_ok=True)


class ReportPDF(FPDF):
    def __init__(self, report_title: str):
        super().__init__()
        self.report_title = report_title

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, self.report_title, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C")

# FPDF standard fonts only support Latin-1.
# This strips emojis and unsupported unicode chars to prevent hard crashes.
def _sanitize_text_for_pdf(text: str) -> str:
    if not isinstance(text, str):
        return str(text)
    return text.encode('latin-1', 'replace').decode('latin-1')


def _generate_sentiment_chart(df: pd.DataFrame, filepath: str):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["date"], df["avg_sentiment"])
    ax.set_title("Daily Average Sentiment")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sentiment Score")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(filepath)
    plt.close(fig)  


def _generate_category_chart(df: pd.DataFrame, filepath: str):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["category"], df["count"])
    ax.set_title("Top Feedback Categories")
    ax.set_ylabel("Count")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(filepath)
    plt.close(fig)  

 # Generates full PDF report and returns filepath.
def generate_feedback_report(days: int = 7) -> str:
    with SessionLocal() as db:
        kpis = get_kpis(db)
        trend_status = get_trend_status(db, days=days)
        ts_df = get_sentiment_timeseries(db, days=days)
        cat_df = get_top_categories(db)
        hp_df = get_high_priority_feedback(db)

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    date_range_str = f"{start_date.date()} to {now.date()}"

    # Defensive Data Conversion for AI 
    top_categories_dict = (
        dict(zip(cat_df["category"], cat_df["count"]))
        if not cat_df.empty
        else {}
    )

    high_priority_examples = (
        hp_df["raw_text"].head(3).tolist()
        if not hp_df.empty
        else []
    )

    # AI Summary
    ai_summary_text = generate_ai_summary(
        date_range=date_range_str,
        kpis=kpis,
        trend_status=trend_status,
        top_categories=top_categories_dict,
        high_priority_examples=high_priority_examples,
    )

    # Generate Charts 
    sentiment_chart_path = os.path.join(REPORTS_DIR, "temp_sentiment.png")
    category_chart_path = os.path.join(REPORTS_DIR, "temp_category.png")

    if not ts_df.empty:
        _generate_sentiment_chart(ts_df, sentiment_chart_path)

    if not cat_df.empty:
        _generate_category_chart(cat_df, category_chart_path)

    # Build PDF 
    report_title = f"Feedback Intelligence Report ({date_range_str})"
    pdf = ReportPDF(report_title)
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Executive Summary
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, f"Report Period: {date_range_str}")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "AI Executive Analysis", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, _sanitize_text_for_pdf(ai_summary_text))
    pdf.ln(6)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(15, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # KPI Section
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Key Metrics", ln=True)
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_font("Helvetica", "", 11)

    pdf.cell(60, 8, "Total Feedback:", 0)
    pdf.cell(0, 8, str(kpis["total_feedback"]), ln=True)

    pdf.cell(60, 8, "Percentage Negative:", 0)
    pdf.cell(0, 8, f"{kpis['percent_negative']}%", ln=True)

    pdf.cell(60, 8, "Average Rating:", 0)
    pdf.cell(0, 8, str(kpis["average_rating"]), ln=True)

    pdf.cell(60, 8, "Trend Status:", 0)
    pdf.cell(0, 8, trend_status, ln=True)
    pdf.ln(8)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    pdf.ln(5)

    # Charts
    if os.path.exists(sentiment_chart_path):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Sentiment Trend", ln=True)
        pdf.ln(3)
        pdf.image(sentiment_chart_path, w=170)
        pdf.ln(8)

    if os.path.exists(category_chart_path):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Top Feedback Categories", ln=True)
        pdf.ln(3)
        pdf.image(category_chart_path, w=170)
        pdf.ln(8)

    # High Priority Table
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "High Priority Feedback", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 10)

    if not hp_df.empty:
        for _, row in hp_df.head(10).iterrows():
            clean_text = _sanitize_text_for_pdf(row["raw_text"][:250])  # limit length
            
            text_block = (
                f"[{row['created_at'].date()}] "
                f"{row['category']} | "
                f"{row['priority_label']} ({round(row['priority_score'], 2)})\n"
                f"{clean_text}\n"
            )
            pdf.multi_cell(0, 5, _sanitize_text_for_pdf(text_block))
            pdf.ln(2)
    else:
        pdf.multi_cell(0, 6, "No high-priority issues detected.")
        pdf.ln(8)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)

    # Save PDF
    filename = f"feedback_report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)
    pdf.output(filepath)

    # Cleanup temp images
    if os.path.exists(sentiment_chart_path):
        os.remove(sentiment_chart_path)
    if os.path.exists(category_chart_path):
        os.remove(category_chart_path)

    return filepath