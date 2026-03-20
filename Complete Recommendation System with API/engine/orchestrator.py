import time
from data.database import get_conn
from data.repositories import MainRepo
from engine.candidate_gen import CandidateGenerator
from engine.scorer import RecommendationScorer
import contextlib

class RecOrchestrator:
    def __init__(self):
        self.repo = MainRepo()
        self.cache = {}
        self.cache_ttl = 300 
        
        # Simple Knowledge Graph for skill relationships
        self.kg = {
            "ai": ["ml", "data", "vision"],
            "web": ["js", "frontend", "backend"],
            "devops": ["backend", "hardware"]
        }

    def get_recs(self, uid, limit=5):
        now = time.time()
        if uid in self.cache:
            ts, recs = self.cache[uid]
            if now - ts < self.cache_ttl:
                return {"data": recs, "cached": True, "ab_group": self.get_ab_group(uid)}

        u_hist = {uid: self.repo.get_user_hist(uid)}
        all_c = self.repo.get_all_content()
        tags = self.repo.get_content_tags()
        
        pop_items = sorted(all_c.keys(), key=lambda x: all_c[x]['popularity'], reverse=True)[:10]

        gen = CandidateGenerator(u_hist, tags, pop_items)
        cands = gen.hybrid_candidates(uid, limit=20)

        with contextlib.closing(get_conn()) as c:
            u_row = c.execute("SELECT interests FROM users WHERE id=?", (uid,)).fetchone()
            base_int = u_row['interests'].split(',') if u_row and u_row['interests'] else []
            
            # Expand interests using Knowledge Graph
            exp_int = set(base_int)
            for i in base_int:
                if i in self.kg:
                    exp_int.update(self.kg[i])

        scorer = RecommendationScorer()

        # A/B Testing logic
        ab_group = self.get_ab_group(uid)

        def match_score(u, i, ctx):
            cat = all_c.get(i, {}).get('category', '')
            return 1.2 if cat in exp_int else 0.1 # Boosted by KG

        def pop_score(u, i, ctx):
            return all_c.get(i, {}).get('popularity', 0.0)

        # Group A gets interest-heavy recs, Group B gets popularity-heavy recs
        if ab_group == "A":
            scorer.add_scorer("kg_interest", match_score, 1.0)
            scorer.add_scorer("popular", pop_score, 0.2)
        else:
            scorer.add_scorer("kg_interest", match_score, 0.5)
            scorer.add_scorer("popular", pop_score, 0.8)

        ranked = scorer.rank_candidates(uid, cands, limit=limit)
        
        res = [{"id": r['item'], "title": all_c[r['item']]['title'], "score": round(r['score'], 2), "reason": r['reason']} for r in ranked]
        self.cache[uid] = (now, res)
        
        return {"data": res, "cached": False, "ab_group": ab_group}

    def get_ab_group(self, uid):
        # basic hash to split users into A or B
        return "A" if hash(uid) % 2 == 0 else "B"

    def add_feedback(self, uid, cid, rating):
        # Real-time personalization (clears cache so next req is instant new rec)
        self.repo.log_interaction(uid, cid, "rating", rating)
        if uid in self.cache: del self.cache[uid] 
        return True