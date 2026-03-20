import heapq

class RecommendationScorer:
    def __init__(self):
        # Simple strategy pattern to hold scoring funcs
        self.scorers = {} 

    def add_scorer(self, name, func, weight=1.0):
        # func should take (uid, iid, ctx) and return 0-1
        self.scorers[name] = (func, weight)

    def calculate_score(self, uid, iid, ctx=None):
        if not self.scorers:
            return 0.0, "no scorers found"

        tot_score = 0.0
        tot_weight = 0.0
        reasons = []

        for name, (func, weight) in self.scorers.items():
            s = func(uid, iid, ctx)
            tot_score += s * weight
            tot_weight += weight
            
            if s > 0:
                reasons.append(f"{name}:{round(s, 2)}")

        final_s = tot_score / tot_weight if tot_weight > 0 else 0.0
        exp = " + ".join(reasons) if reasons else "baseline"
        
        return final_s, f"scored by [ {exp} ]"

    def rank_candidates(self, uid, candidates, limit=10, ctx=None):
        # using heap for fast top-k extraction
        h = []
        
        for iid in candidates:
            score, exp = self.calculate_score(uid, iid, ctx)
            # using score since python only has min-heap built in
            heapq.heappush(h, (-score, iid, exp))
            
        res = []
        # pop the top N items
        for _ in range(min(limit, len(h))):
            neg_s, iid, exp = heapq.heappop(h)
            res.append({"item": iid, "score": -neg_s, "reason": exp})
            
        return res