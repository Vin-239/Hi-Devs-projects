# Resume parsing logic

from core.models import Candidate

# Parses raw resume text and returns a candidate object.
def parse_resume(text):
    # Defaults
    name = "Unknown"
    email = "Unknown"
    education = "Unknown"
    experience = 0
    skills = []

    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        
        if "Name:" in line:
            parts = line.split("Name:", 1)
            if len(parts) > 1:
                name = parts[1].strip()
                
        elif "Email:" in line:
            parts = line.split("Email:", 1)
            if len(parts) > 1:
                email = parts[1].strip()
                
        elif "Education:" in line:
            parts = line.split("Education:", 1)
            if len(parts) > 1:
                education = parts[1].strip()
                
        elif "Experience:" in line:
            parts = line.split("Experience:", 1)
            if len(parts) > 1:
                exp_text = parts[1].strip()
                digits = [char for char in exp_text if char.isdigit()]
                if digits:
                    experience = int("".join(digits))
                    
        elif "Skills:" in line:
            parts = line.split("Skills:", 1)
            if len(parts) > 1:
                raw_skills = parts[1].strip()
                skills = [s.strip().lower() for s in raw_skills.split(",")]

    return Candidate(name, email, skills, experience, education)