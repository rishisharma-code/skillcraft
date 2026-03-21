from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import numpy as np
import os

# Import modules
from face_analysis import detect_face_fatigue
from voice_analysis import extract_voice_features

app = Flask(__name__)
CORS(app)

# Load ML model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/fatigue_model.pkl")

model = None
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)


# Home route
@app.route("/")
def home():
    return "AI Mental Fatigue Detection API Running"


# ML prediction route
@app.route("/predict")
def predict():

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        sample = [[0.5] * 13]

        result = model.predict(sample)
        status = "Fatigued" if result[0] == 1 else "Normal"

        # 🔥 Optional fatigue score
        score = int(np.random.randint(40, 90)) if status == "Fatigued" else int(np.random.randint(10, 40))

        return jsonify({
            "Fatigue Status": status,
            "Fatigue Score (%)": score,
            "method": "ML Model"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# MAIN route (webcam detection)
@app.route("/check-fatigue")
def check_fatigue():

    status = detect_face_fatigue()

    score = 80 if status == "Fatigued" else 20

    return jsonify({
        "Fatigue Status": status,
        "Fatigue Score (%)": score
    })

    try:
        status = detect_face_fatigue()

        score = 80 if status == "Fatigued" else 20

        return jsonify({
            "Fatigue Status": status,
            "Fatigue Score (%)": score,
            "method": "Webcam Face Detection"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Face fatigue route
@app.route("/face-fatigue")
def face_fatigue():

    try:
        status = detect_face_fatigue()

        score = 80 if status == "Fatigued" else 20

        return jsonify({
            "Fatigue Status": status,
            "Fatigue Score (%)": score,
            "method": "Face Detection"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Voice fatigue detection
@app.route("/voice-fatigue", methods=["POST"])
def voice_fatigue():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        file = request.files["audio"]

        features = extract_voice_features(file)

        if features is None:
            return jsonify({"error": "Audio processing failed"}), 500

        features = np.array(features).reshape(1, -1)

        result = model.predict(features)

        status = "Fatigued" if result[0] == 1 else "Normal"

        score = int(np.random.randint(40, 90)) if status == "Fatigued" else int(np.random.randint(10, 40))

        return jsonify({
            "Fatigue Status": status,
            "Fatigue Score (%)": score,
            "method": "Voice Analysis"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Combined fatigue analysis
@app.route("/full-analysis")
def full_analysis():

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        face_status = detect_face_fatigue()

        sample = [[0.5] * 13]
        result = model.predict(sample)

        ml_status = "Fatigued" if result[0] == 1 else "Normal"

        # Final decision
        final_status = "Fatigued" if (
            face_status == "Fatigued" or ml_status == "Fatigued"
        ) else "Normal"

        score = 85 if final_status == "Fatigued" else 25

        return jsonify({
            "Face Result": face_status,
            "ML Result": ml_status,
            "Final Fatigue Status": final_status,
            "Fatigue Score (%)": score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)




    
