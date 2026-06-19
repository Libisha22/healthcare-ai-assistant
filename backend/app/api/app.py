from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)

# 🔥 Enable CORS (fixes frontend issue)
CORS(app)

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "ml", "vectorizer.pkl")

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open(MODEL_PATH, "rb"))
vectorizer = pickle.load(open(VECTORIZER_PATH, "rb"))

# =========================
# HOME ROUTE
# =========================
@app.route("/")
def home():
    return "AI Healthcare API is running"

# =========================
# PREDICT ROUTE
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        symptoms = data.get("symptoms", "")

        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        vector = vectorizer.transform([symptoms])
        prediction = model.predict(vector)[0]

        print("PREDICT API CALLED ✔")

        return jsonify({
            "disease": prediction
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)