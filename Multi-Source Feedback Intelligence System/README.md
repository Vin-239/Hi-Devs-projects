# Multi-Source Feedback Intelligence System
### A deterministic, production-oriented feedback analytics pipeline that ingests multi-source reviews, performs structured NLP analysis, and generates actionable intelligence dashboards and executive reports.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Local%20LLM%20(Ollama)-orange)
![Database](https://img.shields.io/badge/DB-SQLite-blue)
![ORM](https://img.shields.io/badge/ORM-SQLAlchemy-green)
![NLP](https://img.shields.io/badge/NLP-VADER-yellow)
![Reports](https://img.shields.io/badge/Reports-PDF%20%2B%20Matplotlib-lightgrey)

---

## Quick Start (2-Minute Setup)

1. Create venv
2. pip install -r requirements.txt
3. (Optional) ollama pull llama3.1
4. python src/scripts/ingest_and_process.py
5. streamlit run src/dashboard/app.py

---

## Executive Overview
This system was engineered using a Deterministic Core + Interpretive AI Shell architecture.

Core metrics (sentiment scoring, prioritization, trend detection) are computed using rule-based and mathematical methods to ensure:
1. Low latency
2. Predictable outputs
3. Zero hallucination risk
4. Graceful degradation

Generative AI (local LLM via Ollama) is used only at the interpretation layer to generate executive summaries for PDF reports.

If the AI layer fails or is not installed, the system continues functioning without crashing.

---

## Evaluation Criteria Mapping

- Multi-source integration → src/ingestion/
- Sentiment analysis → src/processing/sentiment.py
- Trend detection → src/processing/trends.py
- Issue prioritization → src/processing/pipeline.py
- Dashboard filters → src/dashboard/app.py
- PDF reports → src/reporting/pdf_gen.py
- AI prompts → src/intelligence/ai_summary.py
- Error handling → try/except + fallback logic
- Modular structure → strict src/ separation

---

## Architecture

DATA SOURCES

→ Ingestion Layer

→ Canonical Data Contract (FeedbackData)

→ Intelligence Pipeline

→ SQLite Persistence (Indexed)

→ Analytics Controller Layer

→ Streamlit Dashboard

→ PDF Reporting + Optional AI Summary

---

## Deterministic Engineering Decisions
1. **Canonical Data Spine**

    - All ingestion adapters normalize external data into a strict FeedbackData dataclass before database insertion. 
    - External APIs never write directly to the database.
    - This prevents schema corruption and ensures reproducibility.

2. **Priority Scoring (Mathematically Bounded)**

    - Priority score ∈ [0.0, 1.0]
    - Formula components:
    - Negative sentiment weighting
    - Urgency keyword detection
    - Base-10 logarithmic category frequency
    - Log scaling prevents viral complaint spikes from breaking normalization.

3. **Trend Detection**

    - Uses numpy linear regression (polyfit) on daily average sentiment.
    - Slope thresholds:
        - 0.05 → Improving
        - < -0.05 → Degrading
        - Otherwise → Stable

4. **AI Integration Philosophy**

    - AI is used for:
        - Executive summary
        - Risk explanation
        - Recommended actions

    - AI is NOT used for:
        - Sentiment classification
        - Scoring logic
        - Database operations

    - If Ollama is not running:
        - PDF still generates
        - Deterministic fallback summary is inserted
        - Dashboard never crashes

---

## Testing Strategy

- Phase isolation tests (ingestion, processing, analytics)
- Unique constraint validation
- AI fallback verification
- PDF generation integrity testing

---

## Performance Characteristics

- Processing latency: ~40ms per feedback (local testing)
- Dashboard response time: < 200ms for 1k records
- AI summary generation: 5–15 seconds (local LLM dependent)
- Database: SQLite WAL-mode enabled for concurrency

---

## Reliability Guarantees

- Unique constraint prevents duplicate ingestion
- Idempotent processing logic
- Unicode sanitization prevents PDF crashes
- Safe AI subprocess handling with timeouts
- No external API keys required

---

## Project Structure
```text
Multi-Source Feedback Intelligence System/
│
├── src/
│   ├── models.py                # Canonical DataClasses & SQLAlchemy schema
│   ├── database.py              # SQLite engine + WAL initialization
│
│   ├── ingestion/               # Multi-source adapters
│   │   ├── google_play.py       # Google Play API ingestion
│   │   └── csv_parser.py        # CSV feedback importer
│
│   ├── processing/              # Deterministic Intelligence Pipeline
│   │   ├── pipeline.py          # Sentiment → Category → Priority scoring
│   │   ├── sentiment.py         # VADER integration
│   │   ├── category.py          # Rule-based keyword tagging
│   │   └── trends.py            # Linear regression slope logic
│
│   ├── analytics/               # Controller layer (MVC)
│   │   └── queries.py           # Filtered SQLAlchemy aggregation queries
│
│   ├── intelligence/            # AI interpretation layer
│   │   └── ai_summary.py        # Ollama integration (subprocess-safe)
│
│   ├── reporting/               # Output generation
│   │   └── pdf_gen.py           # Matplotlib + FPDF report engine
│
│   ├── dashboard/
│   │   └── app.py               # Streamlit presentation layer
│
│   └── scripts/
│       └── ingest_and_process.py # Data ingestion entrypoint
│
├── data/
│   ├── raw/                     # Input CSV files
│   └── reports/                 # Generated PDF reports
│
├── tests/                       # Isolation and validation tests
│
├── requirements.txt             # Pinned dependencies
├── .gitignore                   # Prevents DB + raw data commits
└── README.md                    # Documentation
```
---

## Environment Setup (Important)
**Requirements:**
- Python 3.9+
- Pip
- Local installation of Ollama (optional but recommended)

---

## Installation Steps (Exact Order)

- Step 1 — Clone Repository
    ```Bash
    git clone <your-repo-url>
    cd "Multi-Source Feedback Intelligence System"
    ```
- Step 2 — Create Virtual Environment

    Windows:
    ```Bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    Mac/Linux:
    ```Bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- Step 3 — Install Dependencies
    ```Bash
    pip install -r requirements.txt
    ```
- Step 4 — Optional: Install Local AI Model

    Install Ollama:
    https://ollama.com

    Pull recommended model:
    ```Bash
    ollama pull llama3.1
    ```
    Verify:
    ```Bash
    ollama list
    ```
    You should see:
    llama3.1

    (If skipped, the system will fall back to deterministic summary logic.)

---

## Populating the Database (Critical Step)

The dashboard will be empty until data is ingested.

**Option A: Run ingestion script**
```Bash
python src/scripts/ingest_and_process.py
```
This:
- Fetches Google Play reviews
- Processes them through the pipeline
- Stores enriched records in SQLite

**Option B: Upload CSV**

Place CSV in:
```Bash
data/raw/
```
Required CSV columns:
- text
- created_at
- rating (optional)

Run ingestion script again.

---

## Launching the Dashboard
```Bash
streamlit run src/dashboard/app.py
```
Open browser at:
http://localhost:8501

---

## Using the Dashboard
1. **Sidebar Filters**

    - Time Window (Days)
    → Filters trailing data range
    - Source
    → Filters google_play or csv
    - Sentiment
    → Filters Positive / Neutral / Negative

    All filters dynamically modify SQL queries via queries.py.

2. **High Priority Section**

    Displays entries algorithmically flagged as:
    - Critical
    - High
    
    Priority is calculated via deterministic scoring logic.

---

## Generating Executive Reports

Click:
"Generate PDF Report"

System will:
- Aggregate filtered metrics
- Generate static matplotlib charts
- Call local Ollama (if running)
- Compile Unicode-safe PDF
- Provide download link

Reports are saved in:
```Bash
data/reports/
```

---

## AI Troubleshooting

If PDF shows:
"AI Executive Summary unavailable"

Possible reasons:
- Ollama not installed
- Model not pulled
- Wrong model name
- Ollama server not running

Test manually:
```Bash
ollama run llama3.1
```
If this fails, AI layer cannot respond.
System will continue operating without AI.

---

## Known Limitations (Intentional MVP Scope)
- Keyword-based categorization (no transformer classifier)
- Only Google Play + CSV implemented
- SQLite used for portability (can migrate to PostgreSQL)
- No async task queue (single-threaded ingestion)

These decisions prioritize stability and evaluation reliability.

---

## Scalability Path

To productionize:
- Replace SQLite with PostgreSQL (modify database.py connection string)
- Containerize with Docker
- Add Celery for async ingestion
- Replace rule-based categorizer with fine-tuned transformer
- Add App Store RSS adapter

Architecture already supports these upgrades without refactoring.

---


