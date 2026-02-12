# Report generation logic

# Generates a human readable analysis report
def generate_report(candidate, job, score, matched_skills):
    # Ensure matched_skills is always a list
    if matched_skills:
        matched_skills_sorted = sorted(list(matched_skills))
    else:
        matched_skills_sorted = []

    # Structured report data 
    report_data = {
        "candidate_name": candidate.name,
        "email": candidate.email,
        "education": candidate.education,
        "experience_years": candidate.experience,
        "job_title": job.get("title", "Unknown Role"),
        "match_score": score,
        "matched_skills": matched_skills_sorted
    }

    # Recommendation logic 
    if score >= 80:
        recommendation = "STRONGLY RECOMMENDED"
    elif score >= 60:
        recommendation = "RECOMMENDED"
    elif score >= 40:
        recommendation = "REVIEW NEEDED"
    else:
        recommendation = "NOT RECOMMENDED"

    report_data["recommendation"] = recommendation

    # Human readable text report 
    skills_text = ", ".join(matched_skills_sorted) if matched_skills_sorted else "None"

    report_text = (
        "CANDIDATE ANALYSIS REPORT\n"
        f"Name:       {candidate.name}\n"
        f"Role:       {job.get('title', 'Unknown Role')}\n"
        f"Score:      {score}/100\n"
        f"Status:     {recommendation}\n\n"
        f"Matched Skills: {skills_text}\n"
    )

    return report_text, report_data
