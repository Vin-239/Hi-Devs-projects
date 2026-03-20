import sys
import os
# lets scripts import from data folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.database import get_conn
from data.repositories import MainRepo

def seed():
    repo = MainRepo()
    c = get_conn()
    
    # wipe slate clean
    c.executescript("DELETE FROM users; DELETE FROM content; DELETE FROM interactions;")
    
    users = [
        ("u1", "alice", "ai,ml"), ("u2", "bob", "web,js"), ("u3", "charlie", "data,python"),
        ("u4", "dave", "devops"), ("u5", "eve", "ai,vision"), ("u6", "frank", "backend"),
        ("u7", "grace", "frontend"), ("u8", "heidi", "security"), ("u9", "ivan", "mlops"),
        ("u10", "judy", "pc,hardware")
    ]
    c.executemany("INSERT INTO users (id, name, interests) VALUES (?, ?, ?)", users)
    
    content = [
        ("c1", "intro to neural nets", "ai", "beginner", 0.9),
        ("c2", "advanced react", "web", "advanced", 0.8),
        ("c3", "pandas crash course", "data", "beginner", 0.95),
        ("c4", "docker basics", "devops", "beginner", 0.85),
        ("c5", "cv with opencv", "ai", "intermediate", 0.7),
        ("c6", "building rest apis", "backend", "intermediate", 0.88),
        ("c7", "css grid", "web", "beginner", 0.92),
        ("c8", "network security 101", "security", "beginner", 0.75),
        ("c9", "mlops pipelines", "ai", "advanced", 0.6),
        ("c10", "threadripper pc build guide", "hardware", "intermediate", 0.8),
        ("c11", "python generators", "backend", "intermediate", 0.7),
        ("c12", "k8s for beginners", "devops", "intermediate", 0.65),
        ("c13", "sql optimization", "data", "advanced", 0.8),
        ("c14", "malware analysis", "security", "advanced", 0.5),
        ("c15", "vue vs react", "web", "intermediate", 0.77),
        ("c16", "transformers from scratch", "ai", "advanced", 0.9),
        ("c17", "fastapi tutorial", "backend", "beginner", 0.89),
        ("c18", "ci/cd with github actions", "devops", "intermediate", 0.82),
        ("c19", "gpu programming", "hardware", "advanced", 0.6),
        ("c20", "data cleaning tips", "data", "beginner", 0.85)
    ]
    c.executemany("INSERT INTO content (id, title, category, difficulty, popularity) VALUES (?, ?, ?, ?, ?)", content)
    
    interactions = [
        ("u1", "c1", "view", 5.0), ("u1", "c16", "view", 4.5), ("u1", "c9", "view", 4.0),
        ("u2", "c2", "view", 4.0), ("u2", "c7", "view", 5.0),
        ("u3", "c3", "view", 5.0), ("u3", "c13", "view", 4.5),
        ("u9", "c9", "view", 5.0), ("u9", "c4", "view", 4.0),
        ("u10", "c10", "view", 5.0), ("u10", "c19", "view", 4.0)
    ]
    c.executemany("INSERT INTO interactions (user_id, content_id, type, rating) VALUES (?, ?, ?, ?)", interactions)
    
    c.commit()
    print("[+] DB seeded: 10 users, 20 items, and sample interactions ready.")

if __name__ == "__main__":
    seed()