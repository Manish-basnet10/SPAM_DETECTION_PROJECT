"""
Spam Email Detection API
========================
A Flask REST API that uses Machine Learning (Multinomial Naive Bayes) 
to detect spam emails/messages.

Training Method: CountVectorizer + Multinomial Naive Bayes
Dataset: SMS Spam Collection Dataset
Model File: model.pkl
Vectorizer File: vectorizer.pkl

Routes:
- GET /              : API status and documentation
- GET /health        : Health check endpoint
- POST /predict      : Spam prediction endpoint
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== MODEL LOADING ====================
model = None
vectorizer = None
MODEL_READY = False

try:
    # Load pre-trained model and vectorizer from model.pkl (bundled)
    with open("model.pkl", "rb") as model_file:
        bundle = pickle.load(model_file)
    
    # Check if it's a dictionary bundle (model + vectorizer together)
    if isinstance(bundle, dict) and "model" in bundle and "vectorizer" in bundle:
        model = bundle["model"]
        vectorizer = bundle["vectorizer"]
        logger.info("✓ Model and Vectorizer loaded successfully from bundle")
        MODEL_READY = True
    else:
        logger.error("✗ Error: model.pkl does not contain expected 'model' and 'vectorizer' keys")
        MODEL_READY = False
        
except FileNotFoundError as e:
    logger.error(f"✗ Error: Model file not found - {e}")
    logger.error("To generate model files, run: python model.py")
    MODEL_READY = False
except Exception as e:
    logger.error(f"✗ Error loading model: {e}")
    MODEL_READY = False

# ==================== API ROUTES ====================

@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint - Returns API information and available endpoints
    
    Returns:
        JSON with API status, version, and endpoint documentation
    """
    return jsonify({
        "service": "Spam Detection API",
        "status": "running",
        "version": "1.0.0",
        "model_status": "ready" if MODEL_READY else "not loaded",
        "description": "Machine Learning based spam/email detection using Naive Bayes",
        "documentation": {
            "home": {
                "method": "GET",
                "path": "/",
                "description": "API information"
            },
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Health check"
            },
            "predict": {
                "method": "POST",
                "path": "/predict",
                "description": "Predict if message is spam",
                "request_body": {"message": "string"},
                "response": {"result": "Spam or Not Spam"}
            }
        },
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint - Returns API and model status
    
    Returns:
        JSON with health status of API and model
    """
    return jsonify({
        "status": "healthy",
        "api_running": True,
        "model_loaded": MODEL_READY,
        "service": "Spam Detection API",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    """
    Spam Detection Endpoint
    
    Accepts a message and returns whether it's spam or not.
    
    Request Format:
        {
            "message": "The email/message text to check"
        }
    
    Response Format:
        {
            "result": "Spam" or "Not Spam",
            "confidence": percentage,
            "timestamp": "ISO timestamp"
        }
    
    Error Response:
        {
            "error": "Error description",
            "status": "error"
        }
    """
    
    # Handle CORS preflight requests
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    # Validate model is loaded
    if not MODEL_READY:
        return jsonify({
            "status": "error",
            "error": "Model not loaded. Server is not ready."
        }), 503
    
    try:
        # Validate request is JSON
        if not request.is_json:
            return jsonify({
                "status": "error",
                "error": "Request must be JSON with Content-Type: application/json"
            }), 400
        
        data = request.json
        
        # Validate request body is not empty
        if not data:
            return jsonify({
                "status": "error",
                "error": "Empty request body"
            }), 400
        
        # Extract and validate message
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({
                "status": "error",
                "error": "Message field is required and cannot be empty"
            }), 400
        
        # Validate message length
        if len(message) > 5000:
            return jsonify({
                "status": "error",
                "error": "Message is too long (max 5000 characters)"
            }), 400
        
        # Convert message to feature vectors using the vectorizer
        message_vector = vectorizer.transform([message])
        
        # Make prediction using the trained model
        prediction = model.predict(message_vector)[0]
        
        # Convert prediction to readable format (model outputs "spam" or "ham")
        result = "Spam" if prediction.lower() == "spam" else "Not Spam"
        
        # Get prediction probability (if available for this model)
        try:
            probabilities = model.predict_proba(message_vector)[0]
            confidence = round(max(probabilities) * 100, 2)
        except AttributeError:
            # Model doesn't have predict_proba, estimate confidence as 100%
            confidence = 100.0
        
        # Log the prediction
        logger.info(f"Prediction: {result} | Confidence: {confidence}% | Message length: {len(message)}")
        
        # Return prediction result
        return jsonify({
            "status": "success",
            "result": result,
            "confidence": confidence,
            "message_length": len(message),
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except ValueError as e:
        logger.error(f"ValueError during prediction: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"Invalid input: {str(e)}"
        }), 400
    
    except Exception as e:
        logger.error(f"Unexpected error during prediction: {str(e)}")
        return jsonify({
            "status": "error",
            "error": "Internal server error. Please try again later."
        }), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "error": "Endpoint not found",
        "message": "Please check the API documentation"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "status": "error",
        "error": "Method not allowed",
        "message": "Check the documentation for correct HTTP method"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "error": "Internal server error"
    }), 500

# ==================== MAIN ====================

if __name__ == "__main__":
    if MODEL_READY:
        logger.info("=" * 60)
        logger.info("🚀 Spam Detection API starting...")
        logger.info("📍 Server: http://127.0.0.1:5000")
        logger.info("🔗 API Documentation: http://127.0.0.1:5000/")
        logger.info("=" * 60)
        app.run(
            debug=True,
            host="127.0.0.1",
            port=5000,
            use_reloader=True
        )
    else:
        logger.error("Cannot start server: Model files not loaded")
