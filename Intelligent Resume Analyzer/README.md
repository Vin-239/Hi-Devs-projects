# Intelligent Resume Analyzer
### A Deterministic Hiring Pipeline with AI-Augmented Insights

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Local%20LLM%20(Ollama)-orange)
![Status](https://img.shields.io/badge/Status-Capstone%20Complete-green)

---

## Overview
The **Intelligent Resume Analyzer** is a **local, privacy-focused capstone project** that automates candidate screening by combining **deterministic Python logic** with **optional AI-driven qualitative insights**.

The system is deliberately designed to avoid "black-box" decision-making:
* **Deterministic Core:** All scoring and recommendations are computed using transparent, explainable Python rules.
* **Advisory AI:** Generative AI is used *only* as an advisory layer for insights and interview preparation.
* **Zero Bias:** AI output never alters scores or hiring decisions.

*This project was developed as a capstone submission to demonstrate applied Python fundamentals, system design, and responsible AI integration.*

---

## System Architecture

The system follows a linear, fault-tolerant pipeline designed for reproducibility:

```text
[Input] Resume Text / Job Description
           ↓
[Parser]   String Processing Engine
           ↓
[Object]   Candidate Profile (Structured Data)
           ↓
[Matcher]  Deterministic Logic Engine
           ↓
[Result]   Score (0–100) + Matched Skills
           ↓
[Report]   Deterministic Analysis
           ↓
[AI Layer] Optional Insights & Interview Questions
           ↓
[Output]   UI Display + JSON File Persistence
Core Design Principles
Deterministic Core: The same resume + the same job = the same score, every time.

Fail-Soft AI: If the local LLM is unavailable, the system continues gracefully without crashing.

Privacy-First: All data stays on the local machine. No cloud API calls are made.

Syllabus-Aligned: Built using core Python concepts: lists, dictionaries, sets, conditionals, loops, and file I/O.

🛠️ Features & Technical Implementation
1. Robust Resume Parsing
Technique: Line-by-line string processing (split, strip, find).

Robustness: Handles missing fields, variable formatting, and whitespace anomalies.

Concepts: Day 7 (Strings), Day 5 (Loops).

2. Smart Matching Engine
Technique: Skill matching via set intersection; Experience & education checks using conditionals.

Weighting:

Skills: 60%

Experience: 30%

Education: 10%

Concepts: Day 2 (Operators), Day 3 (Conditionals), Day 6 (Sets).

3. AI Advisory Layer (Optional)
Model: qwen2.5 via local Ollama.

Purpose:

Qualitative match insights (Risk/Growth analysis).

Deep, scenario-based interview questions.

Safety: Prompt constraints prevent hallucination; AI never affects deterministic results.

Concepts: Prompt Engineering, Subprocess Management.

📂 Project Structure
Plaintext
resume_analyzer/
│
├── app.py                  # Streamlit UI (Controller & View)
│
├── core/                   # Deterministic Logic
│   ├── parser.py           # Parsing Engine
│   ├── matcher.py          # Scoring Engine
│   ├── reporter.py         # Report Generator
│   └── file_manager.py     # JSON I/O Handler
│
├── ai/                     # Optional AI Advisor
│   ├── client.py           # Robust Ollama Wrapper
│   └── prompts.py          # Prompt Engineering Library
│
├── data/
│   ├── job_description.json
│   └── results/            # Saved Analysis Files
│
└── requirements.txt        # Python Dependencies

---
▶️ How to Run Locally
Prerequisites
Python 3.9+ installed.

Ollama installed locally (required only for AI features).

Step 1: Install Python Dependencies
Bash
pip install -r requirements.txt
Step 2: Setup Local AI (Optional)
Pull the optimized reasoning model used for this project:

Bash
ollama pull qwen2.5
(Note: You can skip this step if you only require deterministic scoring.)

Step 3: Launch the Application
Bash
streamlit run app.py
🧪 Usage Guide
Load Job: Upload a Job Description JSON or paste requirements directly.

Upload Resumes: Select one or multiple .txt resume files.

Toggle AI: Turn on "Qualitative Insights" or "Interview Questions" (optional).

Analyze: Click Analyze Candidates.

View & Save: Expand detailed reports in the UI and find the persistent JSON output in data/results/.

🛡️ Robustness & Safety
This project is engineered to handle edge cases:

Filename Collisions: Auto-timestamps filenames to prevent overwriting data.

Bad Input: Validates JSON schema before processing.

Encoding Issues: Gracefully handles non-UTF-8 characters in resumes.

AI Timeout: Enforces strict timeouts on LLM calls to prevent UI hanging.

Built as a Capstone Project demonstrating Python Proficiency & Systems Thinking.