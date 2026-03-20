# Recommendation Engine Core Components

## Project Overview
This mini-project implements the foundational algorithmic components of a recommendation system. The goal of this project is to simulate how large-scale platforms (like Netflix or Amazon) suggest items to users by building a simple, modular, and working recommendation pipeline. 

The project is broken down into four core modules that handle everything from calculating similarities to evaluating the final recommendations. It uses sample dictionary-based data to demonstrate end-to-end functionality and includes robust error handling for common edge cases.

---

## The Four Core Components

### 1. Similarity Calculator (`similarity.py`)
This module measures how alike two users, items, or skill sets are. 
* **Methods:** Implements `cosine_similarity` for vector comparisons, `jaccard_similarity` for sets/tags, and `pearson_correlation` for rating patterns.
* **Error Handling:** Uses a custom wrapper to safely handle edge cases like empty lists, empty dictionaries, and zero-division errors without crashing.

### 2. Candidate Generator (`candidate_gen.py`)
Before scoring, we need a pool of potential items to evaluate. This module generates those candidates efficiently.
* **Strategies:** Includes collaborative filtering (items liked by similar users), content-based filtering (items matching user history tags), and popularity fallbacks.
* **Functionality:** Features a `hybrid_candidates` method that combines strategies and gracefully handles the "cold start" problem for brand-new users by defaulting to popular items.

### 3. Scorer & Ranker (`scorer.py`)
Not all candidates are equally relevant. This module applies scoring logic and ranks the top picks.
* **Logic:** Uses a flexible strategy pattern to apply different scoring functions with custom weights.
* **Ranking:** Efficiently ranks the scored candidates using a heap data structure to extract the top-K recommendations. It also returns a simple text explanation for *why* an item was recommended.

### 4. Evaluator (`evaluator.py`)
This module checks if our recommendations are actually good by comparing them against ground truth data.
* **Metrics:** Calculates `precision_at_k` (percentage of relevant items in our top picks), `recall_at_k`, and `ndcg_at_k` (which accounts for ranking position).
* **Error Handling:** Safely skips users who lack ground truth data instead of failing the entire evaluation loop.

---

## Code Quality & Functionality
* The codebase relies on standard Python libraries (`math`, `heapq`, `itertools`), ensuring it is lightweight and easy to run without heavy external dependencies.
* Code is kept clean, modular, and lightly commented to explain the core logic.
* All components are designed to plug into each other, passing data from candidate generation -> scoring -> evaluation seamlessly.

---
## How to Run
To verify that all components work together, run the included test script:

```bash
python test.py
```

---

## What the test script does:
1. Loads simple mock data (users, item tags, history).
2. Tests similarity math on sample vectors.
3. Generates a candidate pool for a sample user (u1).
4. Scores and ranks those candidates.
5. Evaluates a set of mock predictions against ground truth data to output performance metrics.


---

## Conclusion & Future Scope
This project successfully demonstrates the core mechanics behind modern recommendation engines. By keeping the architecture modular—separating similarity math, candidate generation, scoring, and evaluation—the system is highly scalable. 

While currently running on simple dictionaries to prove the underlying algorithms, these four components are designed to be easily expanded. In the future, this engine can be hooked up to a real database, integrated with an API, or scaled using more advanced machine learning models without needing to rewrite the foundational logic.

---