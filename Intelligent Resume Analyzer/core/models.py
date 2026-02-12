# Data classes for Candidate and Job

class Candidate:
    def __init__(self, name, email, skills, experience, education):
        self.name = name              
        self.email = email            
        self.skills = skills          
        self.experience = experience  
        self.education = education    

# Converts candidate object to dictionary. Useful for reporting and saving to JSON.
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education
        }
