import math

class RecommendationEvaluator:
    
    def precision_at_k(self, recs, rel_items, k=10):
        if not recs or not rel_items: return 0.0
        
        # grab top k and find intersection
        top_k = set(recs[:k])
        hits = len(top_k & set(rel_items))
        
        return hits / min(k, len(recs))

    def recall_at_k(self, recs, rel_items, k=10):
        if not rel_items: return 0.0
        
        top_k = set(recs[:k])
        hits = len(top_k & set(rel_items))
        
        return hits / len(rel_items)
        
    def ndcg_at_k(self, recs, rel_items, k=10):
        if not recs or not rel_items: return 0.0
        
        # dcg math shortcut
        dcg = 0.0
        for i, r in enumerate(recs[:k]):
            if r in rel_items:
                dcg += 1.0 / math.log2(i + 2) 
                
        # idcg (ideal scenario where all relevant are at the top)
        idcg = 0.0
        ideal_hits = min(len(rel_items), k)
        for i in range(ideal_hits):
            idcg += 1.0 / math.log2(i + 2)
            
        return dcg / idcg if idcg > 0 else 0.0

    def evaluate_all(self, recs_dict, truth_dict, k=10):
        res = {"p_at_k": 0.0, "r_at_k": 0.0, "ndcg": 0.0}
        valid_u = 0
        
        for uid, recs in recs_dict.items():
            # handle missing ground truth
            if uid not in truth_dict or not truth_dict[uid]: 
                continue
                
            rel = truth_dict[uid]
            res["p_at_k"] += self.precision_at_k(recs, rel, k)
            res["r_at_k"] += self.recall_at_k(recs, rel, k)
            res["ndcg"] += self.ndcg_at_k(recs, rel, k)
            
            valid_u += 1
            
        if valid_u == 0: 
            return {"error": "no valid users to eval"}
            
        # get the averages
        for m in res:
            res[m] = round(res[m] / valid_u, 4)
            
        return res