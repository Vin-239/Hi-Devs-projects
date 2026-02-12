# Intelligent Resume Analyzer
### A Deterministic Hiring Pipeline with AI-Augmented Insights

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Local%20LLM%20(Ollama)-orange)

---

## Overview
The **Intelligent Resume Analyzer** is a **local, privacy-focused resume analyzer** that automates candidate screening by combining **deterministic Python logic** with **optional AI-driven qualitative insights**.

The system is deliberately designed to avoid "black-box" decision-making:
* **Deterministic Core:** All scoring and recommendations are computed using transparent, explainable Python rules.
* **Advisory AI:** Generative AI is used *only* as an advisory layer for insights and interview preparation.
* **Zero Bias:** AI output never alters scores or hiring decisions.

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
```
---

## Core Design Principles

1. Deterministic Core: The same resume + the same job = the same score, every time.

2. Fail-Soft AI: If the local LLM is unavailable, the system continues gracefully without crashing.

3. Privacy-First: All data stays on the local machine. No cloud API calls are made.

4. Built using core Python concepts: lists, dictionaries, sets, conditionals, loops, and file I/O.

---

## Features & Technical Implementation

1. Robust Resume Parsing: 
   1. Technique: Line-by-line string processing (split, strip, find).

   2. Robustness: Handles missing fields, variable formatting, and whitespace anomalies.

2. Smart Matching Engine:

   Technique: Skill matching via set intersection; Experience & education checks using conditionals.

   Weighting:

      1. Skills: 60%

      2. Experience: 30%

      3. Education: 10%

4. AI Advisory Layer (Optional):

   Model: qwen2.5 via local Ollama.

   Purpose:

      1. Qualitative match insights (Risk/Growth analysis).

      2. Deep, scenario-based interview questions.

      3. Safety: Prompt constraints prevent hallucination; AI never affects deterministic results.

---
 
## Project Structure
```text
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
│   ├── job_descriptions
│   └── results             # Saved Analysis Files
│   └── resumes
|
└── requirements.txt        # Python Dependencies
```
---

## How to Run Locally

Prerequisites
Python 3.9+ installed.

Ollama installed locally (required only for AI features).


Step 1: Install Python Dependencies
```Bash
pip install -r requirements.txt
```

Step 2: Setup Local AI (Optional)
Pull the optimized reasoning model used for this project:
```Bash
ollama pull qwen2.5
```
(Note: You can skip this step if you only require deterministic scoring.)


Step 3: Launch the Application
```Bash
streamlit run app.py
```
---

## Usage Guide
1. Load Job: Upload one or more Job Description JSON or paste requirements directly.

2. Upload Resumes: Select one or multiple .txt resume files.

3. Toggle AI: Turn on "AI Insights" or "Interview Questions" (optional).

4. Analyze: Click Analyze Candidates.

5. View & Save: Expand detailed reports in the UI and find the persistent JSON output in data/results/.

---

## Robustness & Safety
This project is engineered to handle edge cases:

1. Filename Collisions: Auto-timestamps filenames to prevent overwriting data.

2. Bad Input: Validates JSON schema before processing.

3. Encoding Issues: Gracefully handles non-UTF-8 characters in resumes.

4. AI Timeout: Enforces strict timeouts on LLM calls to prevent UI hanging.

---
*Built as a Capstone Project demonstrating Python Proficiency & Systems Thinking.*
