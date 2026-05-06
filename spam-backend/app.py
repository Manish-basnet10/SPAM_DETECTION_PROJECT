"""
Spam Email Detection API (Production Ready)
Flask + MongoDB + JWT + ML Model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import logging
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# ==================== ENV LOAD ====================
load_dotenv()

# ==================== APP SETUP ====================
app = Flask(__name__)

# CORS (safe for frontend connection)
CORS(app,
     origins="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== CONFIG ====================
JWT_SECRET = os.environ.get("JWT_SECRET", "change_this_secret")
JWT_EXPIRY_HOURS = 24
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")

# ==================== DATABASE ====================
mongo_client = None
db = None
users_col = None
predictions_col = None

try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command("ping")

    db = mongo_client["spam_detection_db"]
    users_col = db["users"]
    predictions_col = db["predictions"]

    users_col.create_index("email", unique=True)

    logger.info("✓ MongoDB Connected")
except Exception as e:
    logger.error(f"MongoDB Error: {e}")

# ==================== ML MODEL ====================
model = None
vectorizer = None
MODEL_READY = False

try:
    with open("model.pkl", "rb") as f:
        bundle = pickle.load(f)

    if isinstance(bundle, dict):
        model = bundle["model"]
        vectorizer = bundle["vectorizer"]
    else:
        model = bundle
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)

    MODEL_READY = True
    logger.info("✓ ML Model Loaded")
except Exception as e:
    logger.error(f"Model Load Error: {e}")

# ==================== JWT ====================
def generate_token(user_id, email, name):
    payload = {
        "user_id": str(user_id),
        "email": email,
        "name": name,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == "OPTIONS":
            return jsonify({"status": "ok"}), 200

        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return wrapper

# ==================== ROUTES ====================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "service": "Spam Detection API",
        "model": "ready" if MODEL_READY else "not loaded"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ==================== PREDICT ====================
@app.route("/predict", methods=["POST", "OPTIONS"])
@require_auth
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if not MODEL_READY:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    try:
        vec = vectorizer.transform([message])
        result_raw = model.predict(vec)[0]

        result = "Spam" if str(result_raw).lower() == "spam" else "Not Spam"

        # Confidence score
        try:
            proba = model.predict_proba(vec)[0]
            confidence = round(float(max(proba)) * 100, 1)
        except Exception:
            confidence = None

        # Save to history
        if predictions_col is not None:
            predictions_col.insert_one({
                "user_id": request.user["user_id"],
                "email": request.user["email"],
                "message": message,
                "result": result,
                "confidence": confidence,
                "created_at": datetime.utcnow()
            })

        return jsonify({
            "result": result,
            "confidence": confidence,
            "message": message
        }), 200

    except Exception as e:
        logger.error(f"Predict Error: {e}")
        return jsonify({"error": "Prediction failed"}), 500


# ==================== REGISTER ====================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    email    = data.get("email", "").strip()
    password = data.get("password", "")
    name     = data.get("name", "").strip()

    if not email or not password or not name:
        return jsonify({"error": "Missing fields"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        result = users_col.insert_one({
            "email": email,
            "password": hashed,
            "name": name,
            "created_at": datetime.utcnow()
        })

        # FIX: return token + user so frontend can auto-login after register
        token = generate_token(result.inserted_id, email, name)

        return jsonify({
            "token": token,
            "user": {
                "id": str(result.inserted_id),
                "name": name,
                "email": email
            }
        }), 201

    except Exception:
        return jsonify({"error": "User already exists"}), 409


# ==================== LOGIN ====================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email    = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    user = users_col.find_one({"email": email})

    if not user:
        return jsonify({"error": "Invalid login"}), 401

    if not bcrypt.checkpw(password.encode(), user["password"]):
        return jsonify({"error": "Invalid login"}), 401

    token = generate_token(user["_id"], user["email"], user["name"])

    # FIX: return token + user object so frontend can store user info
    return jsonify({
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200


# ==================== HISTORY ====================
@app.route("/history", methods=["GET", "OPTIONS"])
@require_auth
def get_history():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        user_id = request.user["user_id"]

        raw = list(
            predictions_col.find(
                {"user_id": user_id},
                {"_id": 0, "message": 1, "result": 1, "confidence": 1, "created_at": 1}
            ).sort("created_at", -1).limit(50)
        )

        # Convert datetime to ISO string for JSON serialisation
        predictions = []
        for p in raw:
            predictions.append({
                "message":    p.get("message", ""),
                "result":     p.get("result", ""),
                "confidence": p.get("confidence"),
                "created_at": p["created_at"].isoformat() if p.get("created_at") else None
            })

        return jsonify({"predictions": predictions}), 200

    except Exception as e:
        logger.error(f"History Error: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500


# ==================== DASHBOARD STATS ====================
@app.route("/dashboard/stats", methods=["GET", "OPTIONS"])
@require_auth
def get_stats():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        user_id = request.user["user_id"]

        total = predictions_col.count_documents({"user_id": user_id})
        spam  = predictions_col.count_documents({"user_id": user_id, "result": "Spam"})
        safe  = total - spam

        recent_raw = list(
            predictions_col.find(
                {"user_id": user_id},
                {"_id": 0, "message": 1, "result": 1, "confidence": 1, "created_at": 1}
            ).sort("created_at", -1).limit(5)
        )

        recent = []
        for p in recent_raw:
            recent.append({
                "message":    p.get("message", ""),
                "result":     p.get("result", ""),
                "confidence": p.get("confidence"),
                "created_at": p["created_at"].isoformat() if p.get("created_at") else None
            })

        return jsonify({
            "stats": {
                "total": total,
                "spam":  spam,
                "safe":  safe
            },
            "recent": recent
        }), 200

    except Exception as e:
        logger.error(f"Stats Error: {e}")
        return jsonify({"error": "Failed to fetch stats"}), 500


# ==================== MAIN ====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)