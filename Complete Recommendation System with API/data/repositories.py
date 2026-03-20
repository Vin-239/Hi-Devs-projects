from data.database import get_conn
import contextlib

class MainRepo:
    def __init__(self):
        self.init_db()
        
    def init_db(self):
        with contextlib.closing(get_conn()) as c:
            c.executescript('''
                CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT, interests TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE IF NOT EXISTS content (id TEXT PRIMARY KEY, title TEXT, category TEXT, difficulty TEXT, popularity REAL);
                CREATE TABLE IF NOT EXISTS skills (id TEXT PRIMARY KEY, name TEXT);
                CREATE TABLE IF NOT EXISTS user_skills (user_id TEXT, skill_id TEXT, proficiency REAL);
                CREATE TABLE IF NOT EXISTS content_skills (content_id TEXT, skill_id TEXT);
                CREATE TABLE IF NOT EXISTS interactions (user_id TEXT, content_id TEXT, type TEXT, rating REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            ''')
            c.commit()
        
    def get_user_hist(self, uid):
        with contextlib.closing(get_conn()) as c:
            rows = c.execute("SELECT content_id FROM interactions WHERE user_id=? AND rating >= 3", (uid,)).fetchall()
            return [r['content_id'] for r in rows]
        
    def get_all_content(self):
        with contextlib.closing(get_conn()) as c:
            rows = c.execute("SELECT * FROM content").fetchall()
            return {r['id']: dict(r) for r in rows}

    def get_content_tags(self):
        with contextlib.closing(get_conn()) as c:
            rows = c.execute("SELECT id, category FROM content").fetchall()
            return {r['id']: [r['category']] for r in rows}

    def log_interaction(self, uid, cid, itype, rating):
        with contextlib.closing(get_conn()) as c:
            c.execute("INSERT INTO interactions (user_id, content_id, type, rating) VALUES (?, ?, ?, ?)", 
                     (uid, cid, itype, rating))
            c.commit()