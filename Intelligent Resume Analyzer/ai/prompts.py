# Prompts for AI analysis and question generation.
class PromptLibrary:
    # Generates the prompt for AI explanation.
    @staticmethod
    def analysis_prompt(candidate, job, report_data):
        skills_text = ", ".join(candidate.skills) if candidate.skills else "None listed"
        matched_text = ", ".join(report_data["matched_skills"]) if report_data["matched_skills"] else "None"

        return f"""
### SYSTEM ROLE
You are a Senior Talent Analyst.
Your job is to interpret data, not just repeat it.
You do NOT make hiring decisions or change scores.

### TRUTH DATA (USE VERBATIM)
- Job Title: {job['title']}
- Required Skills: {', '.join(job['required_skills'])}
- Candidate Skills: {skills_text}
- Matched Skills: {matched_text}
- Experience: {candidate.experience} years
- Calculated Score: {report_data['match_score']}/100

### TASK
Provide 3 qualitative insights about this match.

### STRICT OUTPUT FORMAT
===BEGIN ANALYSIS===
Insight 1: [Analyze the balance of skills vs experience]
Insight 2: [Identify a specific risk or growth area]
Insight 3: [Comment on team fit potential based on skills]
===END ANALYSIS===

### NEGATIVE CONSTRAINTS
- Do NOT recommend hire/reject.
- Do NOT explain or restate the math or value of the score.
- Do NOT invent skills, experience, or personality traits.
- Team fit comments must be based ONLY on skill overlap.
"""


# Generates interview questions. 
    @staticmethod
    def interview_questions_prompt(candidate, job, report_data):
        req_set = set(s.lower() for s in job.get("required_skills", []))
        cand_set = set(s.lower() for s in candidate.skills)
        missing = list(req_set - cand_set)

        # Dynamic Focus Area
        focus_area = ", ".join(missing[:2]) if missing else f"advanced architecture in {job['title']}"

        return f"""
### SYSTEM ROLE
You are a Principal Engineer conducting a technical deep-dive.
Your goal is to expose surface-level knowledge vs deep understanding.

### CONTEXT
- Role: {job['title']}
- Match Score: {report_data['match_score']}
- Missing / Weak Areas: {focus_area}
- Experience: {candidate.experience} years

### TASK
Generate exactly 3 probing interview questions.

### STRICT OUTPUT FORMAT
===BEGIN QUESTIONS===
1. [Conceptual Depth]: Test understanding of {focus_area}.
2. [Scenario]: A real-world production failure or debugging situation.
3. [Trade-off]: A decision requiring judgment (e.g., speed vs reliability).
===END QUESTIONS===

### NEGATIVE CONSTRAINTS
- Do NOT ask generic "What is X?" questions.
- Do NOT provide answers.
- Do NOT introduce new skills or assumptions.
- Do NOT be polite or verbose. Just list the questions.
"""
