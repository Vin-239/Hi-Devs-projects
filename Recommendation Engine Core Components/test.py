from similarity import SimilarityCalculator
from candidate_gen import CandidateGenerator
from scorer import RecommendationScorer
from evaluator import RecommendationEvaluator

# dummy data to test everything
u_hist = {
    "u1": ["i1", "i2", "i3"],
    "u2": ["i2", "i3", "i4"],
    "u3": ["i5", "i6"]
}

i_tags = {
    "i1": ["ai", "tech"],
    "i2": ["tech", "coding"],
    "i3": ["ai", "data"],
    "i4": ["hardware", "pc"],
    "i5": ["web", "design"],
    "i6": ["web", "js"]
}

pop = ["i2", "i3", "i1", "i5"]
truth = {"u1": ["i4"], "u2": ["i1", "i5"]}

print("--- 1. Testing Sim ---")
sim = SimilarityCalculator()
v1, v2 = {"i1": 5, "i2": 3}, {"i1": 4, "i2": 4, "i3": 1}
print(f"Cos Sim: {round(sim.cosine_similarity(v1, v2), 2)}")
print(f"Jac Sim: {sim.jaccard_similarity(set(i_tags['i1']), set(i_tags['i2']))}")

print("\n--- 2. Testing Cands ---")
gen = CandidateGenerator(u_hist, i_tags, pop)
cands_u1 = gen.hybrid_candidates("u1", limit=5)
print(f"U1 cands: {cands_u1}")

print("\n--- 3. Testing Scorer ---")
scorer = RecommendationScorer()

# simple mock scoring func
def mock_score(uid, iid, ctx):
    return 1.0 if "ai" in i_tags.get(iid, []) else 0.5

scorer.add_scorer("ai_match", mock_score, 1.0)
ranked = scorer.rank_candidates("u1", cands_u1, limit=3)

print("U1 Ranked:")
for r in ranked: 
    print(r)

print("\n--- 4. Testing Eval ---")
ev = RecommendationEvaluator()
# mock preds
preds = {"u1": ["i4", "i2"], "u2": ["i1", "i5", "i6"]}
metrics = ev.evaluate_all(preds, truth, k=2)
print(f"Metrics: {metrics}")
print("\n[+] all tests ran successfully.")
