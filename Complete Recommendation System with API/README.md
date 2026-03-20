# **Complete Recommendation System with API**

## **Project Overview**
This project is a complete, production-ready recommendation system microservice. It integrates core recommendation algorithms with a Flask-based REST API and an SQLite database. The system is designed to simulate how large-scale platforms serve personalized content by handling real-world challenges such as cold-start users, dynamic caching, real-time feedback processing, and high-concurrency request loads. 

The final product is a robust, full-stack pipeline demonstrating data modeling, API development, system integration, and performance testing.

---

## **Key Features & Capabilities**
* **Hybrid Recommendation Engine:** 
Combines collaborative filtering, content-based filtering, and popularity fallbacks to generate candidate pools.
* **Intelligent Scoring & Ranking:** Utilizes a Strategy pattern to apply weighted scoring (interest matching, popularity) and extracts top-K recommendations efficiently.
* **Cold Start Handling:** Seamlessly falls back to popularity-based and metadata-driven recommendations for new users with no interaction history.

* **Caching Layer:** Implements an in-memory TTL (Time-To-Live) cache to achieve sub-20ms response times under load, which instantly invalidates when a user submits new feedback.
* **Knowledge Graph Integration:** Uses a dictionary-based knowledge graph to map related skills (e.g., matching "ml" to "ai") for deeper personalization.
* **A/B Testing Framework:** Dynamically segments users into groups to test different scoring weights (e.g., interest-heavy vs. popularity-heavy).
* **Frontend Dashboard:** Includes a lightweight HTML/JS dashboard served at the root URL to visually interact with the API.

---

## **System Architecture**

The codebase is organized into a modular, microservice-style architecture:
### **Complete File Structure**
```text
day10_capstone/
├── api/
│   ├── __init__.py
│   └── app.py                 # Flask REST API, routing, request tracing
├── data/
│   ├── __init__.py
│   ├── database.py            # SQLite connection manager
│   ├── models.py              # DataClasses for schemas
│   └── repositories.py        # Repository pattern for DB operations
├── engine/
│   ├── __init__.py
│   ├── candidate_gen.py       # Candidate generation strategies
│   ├── evaluator.py           # Metrics calculation (Precision, Recall, NDCG)
│   ├── orchestrator.py        # Connects DB, caching, and recommendation logic
│   ├── scorer.py              # Scoring and ranking logic via Heap
│   └── similarity.py          # Similarity math (Cosine, Jaccard, Pearson)
├── scripts/
│   ├── __init__.py
│   ├── evaluate.py            # Performance evaluation and load testing script
│   └── seed_data.py           # Script to populate initial DB state
├── tests/
│   ├── __init__.py
│   └── test_api.py            # Unit and integration tests
├── Procfile                   # Deployment configuration for cloud hosting
├── README.md                  # Project documentation
├── evaluation_report.md       # Auto-generated performance results
├── postman_collection.json    # Importable API test suite
├── rec_sys.db                 # SQLite database file
└── requirements.txt           # Python dependencies

```
---

## **Database Schema (SQLite)**
The data layer is fully normalized and managed via a Repository pattern to abstract SQL queries from the application logic.
* **users** (id, name, interests, created_at)
* **content** (id, title, category, difficulty, popularity)
* **skills** (id, name)
* **user_skills** (user_id, skill_id, proficiency)
* **content_skills** (content_id, skill_id)
* **interactions** (user_id, content_id, type, rating, created_at)

---

## **Setup & Installation**
**1. Install Dependencies**
Ensure you have Python 3.8+ installed. Install the required packages:

```Bash
pip install -r requirements.txt
```

**2. Seed the Database**
Populate the SQLite database with the rich sample dataset (10 users, 20 AI/Tech content items, and realistic interactions):

```Bash
python scripts/seed_data.py
```

**3. Run the Automated Evaluation & Load Test**
Verify the system's accuracy and performance. This script will simulate 10 concurrent users and generate an ```evaluation_report.md``` file:

```Bash
python scripts/evaluate.py
```

**4. Run the Unit Tests**
Ensure all API endpoints and core logic handle edge cases correctly (80%+ coverage):

```Bash
python -m unittest tests.test_api
```

**5. Start the Server**
Launch the Flask application:

```Bash
python -m api.app
```

The API and Frontend Dashboard will be available at ```http://127.0.0.1:5000```.

---

## **API Documentation**
All endpoints return JSON and include a unique ```X-Request-Id``` header for production request tracing.

**1. Get Recommendations**

Retrieves a personalized list of content items for a specific user.

* **Endpoint:** ```GET /recommend/<user_id>```
* **Query Parameters:** ```limit```(optional, default=5)
* **Response (200 OK):**

    ```JSON
    {
    "req_id": "a1b2c3d4",
    "user_id": "u1",
    "ab_group": "A",
    "cached": false,
    "recommendations": [
        {
        "id": "c16",
        "title": "transformers from scratch",
        "score": 1.25,
        "reason": "scored by [ kg_interest:1.2 + popular:0.9 ]"
        }
    ]
    }
    ```
* **Error States:** Returns ```404 Not Found``` if the user ID does not exist in the database.

**2. Submit Feedback**

Logs a user interaction (e.g., rating an item). This automatically clears the user's cache to ensure the next recommendation request reflects this new data in real-time.

* **Endpoint:** ```POST /feedback```

* **Payload:**

    ```JSON
    {
    "uid": "u1",
    "cid": "c5",
    "rating": 5.0
    }
    ```
* **Response (201 Created):** ```{"msg": "feedback logged", "req_id": "..."}```

* **Error States:** Returns ```400 Bad Request``` if payload is missing required fields.

**3. System Health**
* **Endpoint:** ```GET /health```
* **Response (200 OK):** ```{"status": "ok", "engine": "running"}```

**4. System Metrics**
* **Endpoint:** ```GET /metrics```
* **Response (200 OK):** ```{"uptime_sec": 120.5, "total_requests": 45, "errors": 0}```

---

## **Evaluation & Performance Metrics**
The system is continuously evaluated using offline metrics via ```scripts/evaluate.py```. Based on the latest evaluation run:

1. **Accuracy Metrics (k=5):**
    * Precision@5: 0.4667
    * Recall@5: 0.7778
    * NDCG@5: 0.7163

2. **Performance / Throughput:**  Load tested with 10 concurrent threads.
    * Average Response Time: ~17.48ms (Significantly outperforming the <200ms target).

---

## **Conclusion & Future Scope**
This Capstone project successfully bridges the gap between theoretical machine learning algorithms and production software engineering. By isolating the data, engine, and API layers, the system is highly modular and ready to scale.

While currently relying on an SQLite database and in-memory caching to demonstrate end-to-end functionality, the architecture is designed so that these components can be seamlessly swapped for enterprise tools (e.g., PostgreSQL, Redis) without altering the core recommendation engine logic.

---