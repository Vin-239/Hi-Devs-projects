import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
import threading
import urllib.request
from engine.evaluator import RecommendationEvaluator
from engine.orchestrator import RecOrchestrator

def run_metrics():
    print("--- 1. Offline Metrics ---")
    orch = RecOrchestrator()
    ev = RecommendationEvaluator()
    
    truth = {"u1": ["c9", "c16", "c1"], "u2": ["c2", "c7", "c15"], "u3": ["c3", "c13", "c20"]}
    preds = {}
    for u in truth.keys():
        recs = orch.get_recs(u, limit=5)["data"]
        preds[u] = [r["id"] for r in recs]
        
    res = ev.evaluate_all(preds, truth, k=5)
    print(f"P@5: {res.get('p_at_k',0)}, R@5: {res.get('r_at_k',0)}, NDCG@5: {res.get('ndcg',0)}")
    return res

def run_load_test():
    print("\n--- 2. Load Test (10 concurrent users) ---")
    url = "http://127.0.0.1:5000/recommend/u1"
    
    try: urllib.request.urlopen(url)
    except: pass

    times = []
    def fetch():
        st = time.time()
        try:
            urllib.request.urlopen(url)
            times.append(time.time() - st)
        except Exception as e: print("req failed:", e)
            
    threads = [threading.Thread(target=fetch) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    avg_ms = (sum(times) / len(times)) * 1000 if times else 0
    print(f"Avg Response Time: {avg_ms:.2f}ms")
    return avg_ms

if __name__ == "__main__":
    m = run_metrics()
    t = run_load_test()
    
    status = 'PASS' if t < 200 else 'FAIL'
    md = f"""# System Evaluation Report

## 1. Accuracy Metrics (k=5)
| Metric | Score |
|---|---|
| Precision@5 | {m.get('p_at_k', 0)} |
| Recall@5 | {m.get('r_at_k', 0)} |
| NDCG@5 | {m.get('ndcg', 0)} |

## 2. Performance Metrics
* **Concurrent Users:** 10
* **Avg Response Time:** {t:.2f} ms
* **Status:** {status} (Target < 200ms)
"""
    with open("evaluation_report.md", "w") as f:
        f.write(md)
    print("\n[+] evaluation_report.md generated successfully!")