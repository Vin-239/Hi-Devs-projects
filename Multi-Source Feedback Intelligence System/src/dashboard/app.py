import sys
import os

# Ensure project root is discoverable
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

import streamlit as st
import plotly.express as px

from src.database import init_db, SessionLocal
from src.analytics.queries import (
    get_kpis,
    get_sentiment_timeseries,
    get_trend_status,
    get_top_categories,
    get_high_priority_feedback,
)
from src.reporting.pdf_gen import generate_feedback_report

# Initialization
init_db()

st.set_page_config(
    page_title="Feedback Intelligence System",
    layout="wide"
)

st.title("AI-Powered Feedback Intelligence System")

# Sidebar Filters
st.sidebar.header("Filters")

days_filter = st.sidebar.slider(
    "Time Window (Days)",
    min_value=7,
    max_value=90,
    value=30,
)

source_filter = st.sidebar.selectbox(
    "Source",
    ["All", "google_play", "csv"]
)

sentiment_filter = st.sidebar.selectbox(
    "Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)

# Convert UI to backend-compatible values
source_value = None if source_filter == "All" else source_filter
sentiment_value = None if sentiment_filter == "All" else sentiment_filter

# Data Fetching
with SessionLocal() as db:

    kpis = get_kpis(
        db,
        source=source_value,
        sentiment=sentiment_value,
    )

    trend_status = get_trend_status(
        db,
        days=days_filter,
        source=source_value,
        sentiment=sentiment_value,
    )

    ts_df = get_sentiment_timeseries(
        db,
        days=days_filter,
        source=source_value,
        sentiment=sentiment_value,
    )

    cat_df = get_top_categories(
        db,
        source=source_value,
        sentiment=sentiment_value,
    )

    hp_df = get_high_priority_feedback(
        db,
        source=source_value,
        sentiment=sentiment_value,
    )

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Feedback", kpis["total_feedback"])
col2.metric("% Negative", f"{kpis['percent_negative']}%")
col3.metric("Average Rating", kpis["average_rating"])
col4.metric("Trend", trend_status)

st.divider()

# Sentiment Trend Chart
st.subheader("Sentiment Trend Over Time")

if ts_df.empty:
    st.info("No data available for selected filters.")
else:
    fig = px.line(
        ts_df,
        x="date",
        y="avg_sentiment",
        markers=True,
        title="Daily Average Sentiment"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Category Distribution
st.subheader("Top Feedback Categories")

if cat_df.empty:
    st.info("No category data available.")
else:
    fig_cat = px.bar(
        cat_df,
        x="category",
        y="count",
        title="Most Frequent Categories",
        color="category"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# High Priority Feedback Table
st.subheader("High Priority Feedback")

if hp_df.empty:
    st.info("No high priority issues detected.")
else:
    st.dataframe(hp_df, use_container_width=True)

st.divider()

# PDF Report Section
st.subheader("Generate Executive Report")

if st.button("Generate PDF Report"):

    with st.spinner("Generating report..."):
        try:
            report_path = generate_feedback_report(days=days_filter)

            st.success("Report generated successfully.")

            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download PDF Report",
                    data=file,
                    file_name=os.path.basename(report_path),
                    mime="application/pdf",
                )

        except Exception as e:
            st.error(f"Report generation failed: {e}")