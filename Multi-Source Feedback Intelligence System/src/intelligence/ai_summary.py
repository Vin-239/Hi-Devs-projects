import subprocess
import shutil
import os
from typing import Dict
from datetime import datetime


DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
TIMEOUT_SECONDS = 60 #seconds

# Build structured prompt for executive-grade report generation.
def _build_prompt(date_range: str,kpis: Dict,trend_status: str,top_categories: Dict[str, int],high_priority_examples: list[str],) -> str:
    category_lines = "\n".join(
        [f"- {cat}: {count} reports" for cat, count in top_categories.items()]
    )

    examples_text = "\n".join(
        [f"- \"{text[:200]}\"" for text in high_priority_examples]
    )

    prompt = f"""
You are a senior product intelligence analyst writing for executive stakeholders.

Generate a professional product feedback intelligence report.

Report Context:
Time Range: {date_range}

KPIs:
- Total Feedback: {kpis.get("total_feedback", 0)}
- Percentage Negative: {kpis.get("percent_negative", 0)}%
- Average Rating: {kpis.get("average_rating", 0)}
- Trend Direction: {trend_status}

Top Categories:
{category_lines if category_lines else "No significant category spikes."}

Sample High-Priority Feedback:
{examples_text if examples_text else "No critical issues detected."}

Instructions:
1. Write a 2-paragraph Executive Summary.
2. Provide 3–5 Key Risks.
3. Provide 3–5 Recommended Actions.
4. Identify any Emerging Patterns.

Be concise, analytical, and business-focused.
Avoid fluff.
"""
    return prompt.strip()

# Calls local Ollama to generate executive summary.
# Returns text summary. Falls back gracefully if Ollama unavailable.
def generate_ai_summary(date_range: str,kpis: Dict,trend_status: str,top_categories: Dict[str, int],high_priority_examples: list[str],) -> str:
    if shutil.which("ollama") is None:
        return "AI unavailable: Ollama CLI not found."
    
    prompt = _build_prompt(
        date_range=date_range,
        kpis=kpis,
        trend_status=trend_status,
        top_categories=top_categories,
        high_priority_examples=high_priority_examples,
    )

    try:
        process = subprocess.run(
            ["ollama", "run", DEFAULT_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=TIMEOUT_SECONDS,
            check=False
        )

        if process.returncode != 0:
            stderr = (process.stderr or "").lower()
            if "not found" in stderr:
                return f"Model '{DEFAULT_MODEL}' not found. Run: ollama pull {DEFAULT_MODEL}"
            return _fallback_summary(kpis, trend_status)

        output = process.stdout.strip()

        if not output:
            return _fallback_summary(kpis, trend_status)

        return output
    
    except subprocess.TimeoutExpired:
        return _fallback_summary(kpis, trend_status)

    except Exception:
        return _fallback_summary(kpis, trend_status)

# Deterministic fallback summary if AI is unavailable.
# Provides key insights based on KPIs and trend status. 
# Ensures executives still receive actionable information.
def _fallback_summary(kpis: Dict, trend_status: str) -> str:
    return f"""
Executive Summary (AI unavailable)

During the selected reporting period, the system processed {kpis.get('total_feedback', 0)} feedback entries.
Overall negative sentiment stands at {kpis.get('percent_negative', 0)}%.
The average rating recorded was {kpis.get('average_rating', 0)}.

Trend analysis indicates a '{trend_status}' direction in customer sentiment.
Teams should monitor high-priority issues and investigate recurring categories
to prevent further degradation in user experience.
""".strip()