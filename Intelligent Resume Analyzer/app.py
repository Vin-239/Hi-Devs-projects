# Streamlit UI for Intelligent Resume Analyzer

import streamlit as st
import json
import os
import time

from core.parser import parse_resume
from core.matcher import match_candidate
from core.reporter import generate_report
from core.file_manager import save_results, load_json

# Import AI Layer (if available) - This is optional and won't break the app if missing.
try:
    from ai.client import OllamaClient
    from ai.prompts import PromptLibrary
    AI_MODULE_PRESENT = True
except ImportError:
    AI_MODULE_PRESENT = False

if not AI_MODULE_PRESENT:
    use_ai_explanation = False
    use_ai_questions = False

# Page configuration
st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="IRA",
    layout="centered"
)

st.title("Intelligent Resume Analyzer")
st.markdown("---")
st.info("Upload resumes and provide one or more job descriptions to analyze.")

# Job description input
st.subheader("Job Description")

job_upload = st.file_uploader(
    "Upload Job Description (.json)",
    type=["json"],
    help="You can upload a single job object or a list of job objects. "
)

default_job = load_json("data/job_description.json", default={})
default_text = json.dumps(default_job, indent=4)

job_json_input = st.text_area(
    "or Paste Job Description JSON (single job or list of jobs)",
    value=default_text,
    height=250,
    help="If a file is uploaded above, this text area will be ignored."
)

# Resume upload
st.subheader("Candidate Resumes")

uploaded_files = st.file_uploader(
    "Upload Resume(s) (.txt only)",
    type=["txt"],
    accept_multiple_files=True,
    help="You can select multiple files at once. Ensure the file is a standard text file (UTF-8)."
)

#Normalizes job description into the schema expected by the core matcher.
def normalize_job(job_data):
    if not isinstance(job_data, dict):
        return None

    skills = job_data.get("required_skills") or job_data.get("skills") or []
    if not isinstance(skills, list):
        skills = []

    # Safe Integer Conversion (Loophole 1 Fix)
    try:
        min_exp = int(job_data.get("min_experience_years", 0))
    except (ValueError, TypeError):
        min_exp = 0

    return {
        "title": job_data.get("title", "Unknown Role"),
        "min_experience_years": min_exp,
        "required_education": job_data.get("required_education", ""),
        "required_skills": skills
    }

def ai_ready(client):
    try:
        if client is None:
            return False
        return hasattr(client, "_ollama_exists") and client._ollama_exists()
    except Exception:
        return False

# AI Settings (Toggles)
st.subheader("AI Assistance (Optional)")
ai_col1, ai_col2 = st.columns(2)
with ai_col1:
    use_ai_explanation = st.toggle(
        "AI Insights (Qualitative)", 
        value=False, 
        disabled=not AI_MODULE_PRESENT
    )
with ai_col2:
    use_ai_questions = st.toggle(
        "Interview Questions", 
        value=False, 
        disabled=not AI_MODULE_PRESENT
    )

# Check connectivity immediately if toggles are on
if (use_ai_explanation or use_ai_questions) and AI_MODULE_PRESENT:
    client = OllamaClient()
    if not ai_ready(client):
        st.error("Ollama not found! AI features will be disabled.")
        client = None
    else:
        st.caption("Local AI Agent Ready")
else:
    client = None

# Analyze button
if st.button("Analyze Candidate", type="primary"):

    # Input validation
    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    if not job_json_input.strip() and not job_upload:
        st.warning("Please provide a job description (paste or upload).")
        st.stop()

    # Load job description
    try:
        if job_upload:
            job_data = json.load(job_upload)
            st.caption("Using uploaded job description file.")
        else:
            job_data = json.loads(job_json_input)
            st.caption("Using pasted job description text.")
    except json.JSONDecodeError:
        st.error("Invalid job description JSON. Please check syntax.")
        st.stop()

    # Normalize job_data to a list
    if isinstance(job_data, dict):
        jobs = [job_data]
    elif isinstance(job_data, list):
        jobs = job_data
    else:
        st.error("Job description must be a JSON object or list of objects.")
        st.stop()

    # Pre-process and validate jobs
    valid_jobs = []
    for raw_job in jobs:
        clean_job = normalize_job(raw_job)
        if clean_job:
            valid_jobs.append(clean_job)
    if not valid_jobs:
        st.error("No valid job descriptions found. Please check your JSON input.")
        st.stop()

    # Decode resume
    for uploaded_file in uploaded_files:
        
        # Read & Parse Resume
        try:
            uploaded_file.seek(0)
            resume_text = uploaded_file.read().decode("utf-8")
            candidate = parse_resume(resume_text)
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {e}")
            continue

        candidate_reports = []
        
        # Match against all jobs
        for job in valid_jobs:
            score, matched_skills = match_candidate(candidate, job)
            report_text, report_data = generate_report(
                candidate, job, score, matched_skills
            )

            # AI analysis (if enabled and client is available)
            if client:
                with st.spinner(f"Consulting AI for {candidate.name}..."):
                    
                    # Explanation
                    if use_ai_explanation:
                        prompt = PromptLibrary.analysis_prompt(candidate, job, report_data)
                        report_data["ai_explanation"] = client.generate_analysis(prompt)
                    
                    # Interview questions
                    if use_ai_questions:
                        q_prompt = PromptLibrary.interview_questions_prompt(candidate, job, report_data)
                        report_data["ai_interview_questions"] = client.generate_questions(q_prompt)

            candidate_reports.append((report_text, report_data))

        # Save Results (Per Candidate)
        save_cand_name = candidate.name.replace(" ", "_").lower()
        if "unknown" in save_cand_name: 
            save_cand_name = "resume"
            
        safe_filename = uploaded_file.name.replace(".txt", "").replace(" ", "_").lower()
        timestamp = int(time.time())
        final_filename = f"{save_cand_name}_{safe_filename}_{timestamp}_analysis.json"
            
        output_file = os.path.join("data", "results", final_filename)
        
        # Save just the data dicts
        save_results([r[1] for r in candidate_reports], output_file)

        # Display Results (Per Candidate)
        with st.container():
            st.markdown("---")
            st.header(f"Name: {candidate.name}")
            st.caption(f"Source: {uploaded_file.name} | Experience: {candidate.experience} Years")

            # Create columns for multiple job matches
            for i, (rep_text, rep_data) in enumerate(candidate_reports):
                job_title = rep_data.get('job_title', 'Job')
                score = rep_data.get('match_score', 0)
                rec = rep_data.get('recommendation', 'N/A')
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                        st.subheader(f"{job_title}")
                        st.caption(f"Status: {rec}")
                        
                with col2:
                        st.metric("Match Score", f"{score}/100")
                        
                with st.expander("View Details"):
                    st.code(rep_text)
            
                if rep_data.get("ai_explanation"):
                    st.info(f"AI Analysis: \n\n{rep_data['ai_explanation']}")
                
                if rep_data.get("ai_interview_questions"):
                    with st.expander("AI Interview Questions"):
                        st.markdown(rep_data['ai_interview_questions'])
            
            st.success(f"Saved analysis to `{output_file}`")
