from flask import Flask, request, jsonify, render_template_string
import uuid
import time
import contextlib
from engine.orchestrator import RecOrchestrator
from data.database import get_conn

app = Flask(__name__)
orch = RecOrchestrator()

metrics = {"total_reqs": 0, "errors": 0, "start_time": time.time()}

@app.before_request
def pre_req():
    request.id = uuid.uuid4().hex[:8]
    request.start = time.time()

@app.after_request
def post_req(resp):
    dur = round((time.time() - request.start) * 1000, 2)
    metrics["total_reqs"] += 1
    resp.headers['X-Request-Id'] = request.id
    return resp

# Simple Frontend Dashboard
HTML_DASH = """
<!DOCTYPE html>
<html><head><title>Rec Engine Dash</title><style>body{font-family:sans-serif; max-width:600px; margin:40px auto;}</style></head>
<body>
    <h2>User Recommendations</h2>
    <input id="uid" type="text" value="u1" placeholder="User ID">
    <button onclick="getRecs()">Get Recs</button>
    <div id="out" style="margin-top:20px; padding:10px; background:#f4f4f4; border-radius:5px;"></div>
    <script>
        async function getRecs() {
            let uid = document.getElementById('uid').value;
            let res = await fetch('/recommend/' + uid);
            let data = await res.json();
            document.getElementById('out').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        }
    </script>
</body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_DASH)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "engine": "running"}), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    up = round(time.time() - metrics["start_time"], 2)
    return jsonify({"uptime_sec": up, "total_requests": metrics["total_reqs"], "errors": metrics["errors"]}), 200

@app.route('/recommend/<uid>', methods=['GET'])
def recommend(uid):
    try:
        with contextlib.closing(get_conn()) as c:
            u = c.execute("SELECT id FROM users WHERE id=?", (uid,)).fetchone()
            if not u:
                metrics["errors"] += 1
                return jsonify({"err": "user not found"}), 404

        limit = int(request.args.get('limit', 5))
        recs = orch.get_recs(uid, limit)
        
        return jsonify({
            "req_id": request.id,
            "user_id": uid,
            "ab_group": recs["ab_group"],
            "cached": recs["cached"],
            "recommendations": recs["data"]
        }), 200
    except Exception as e:
        metrics["errors"] += 1
        return jsonify({"err": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    if not data or 'uid' not in data or 'cid' not in data or 'rating' not in data:
        metrics["errors"] += 1
        return jsonify({"err": "missing payload"}), 400
    try:
        orch.add_feedback(data['uid'], data['cid'], float(data['rating']))
        return jsonify({"msg": "feedback logged", "req_id": request.id}), 201
    except Exception:
        metrics["errors"] += 1
        return jsonify({"err": "failed to save"}), 500

if __name__ == '__main__':
    # threaded=True handles concurrent requests better
    app.run(debug=True, port=5000, threaded=True)