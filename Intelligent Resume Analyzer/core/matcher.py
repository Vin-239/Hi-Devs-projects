# Scoring and matching algorithms

# Compares candidate profile with job requirements and returns (score, matched_skills)
def match_candidate(candidate, job):
    score = 0.0 

    # Skill matching (60 points max)
    candidate_skills = set(s.lower() for s in candidate.skills)
    job_skills_raw = job.get("required_skills", [])
    job_skills = set(s.lower() for s in job_skills_raw)
    matched_skills = candidate_skills & job_skills

    if job_skills:
        match_percentage = len(matched_skills) / len(job_skills)
        score += match_percentage * 60

    # Experience check (30 points max)
    min_exp = job.get("min_experience_years", 0)
    
    if candidate.experience >= min_exp:
        score += 30
    elif candidate.experience > 0:
        score += 10  

    # Education check (10 points max)
    required_edu = job.get("required_education", "")

    if required_edu and required_edu.lower() in candidate.education.lower():
        score += 10
    score = min(score, 100)
    final_score = round(score, 1)

    return final_score, list(matched_skills)
