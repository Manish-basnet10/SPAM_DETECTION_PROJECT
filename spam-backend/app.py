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
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# ==================== ENV LOAD ====================
load_dotenv()

# ==================== APP SETUP ====================
app = Flask(__name__)

CORS(app,
     origins="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

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


@app.route("/predict", methods=["POST", "OPTIONS"])
@require_auth
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if not MODEL_READY:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Empty message"}), 400

    vec = vectorizer.transform([message])
    result_raw = model.predict(vec)[0]

    result = "Spam" if str(result_raw).lower() == "spam" else "Not Spam"

    return jsonify({
        "result": result,
        "message": message
    })


# ==================== AUTH (BASIC) ====================

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = data["password"]
    name = data["name"]

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    users_col.insert_one({
        "email": email,
        "password": hashed,
        "name": name
    })

    return jsonify({"message": "User created"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_col.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "Invalid login"}), 401

    if not bcrypt.checkpw(data["password"].encode(), user["password"]):
        return jsonify({"error": "Invalid login"}), 401

    token = generate_token(user["_id"], user["email"], user["name"])

    return jsonify({"token": token})


# ==================== MAIN (IMPORTANT FIX) ====================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)