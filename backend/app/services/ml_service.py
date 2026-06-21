import json
import pickle

with open("app/ml/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("app/ml/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("data/disease_info.json", "r") as f:
    disease_info = json.load(f)

print("ML Service Loaded")

def predict_disease(symptoms: str):

    transformed = vectorizer.transform([symptoms])

    probabilities = model.predict_proba(transformed)[0]

    classes = model.classes_

    results = []

    for disease, prob in zip(classes, probabilities):

        info = disease_info.get(disease, {})

        results.append({
            "disease": disease,
            "confidence": round(prob * 100, 2),
            "description": info.get("description"),
            "severity": info.get("severity"),
            "doctor": info.get("doctor"),
            "medicines": info.get("medicines"),
            "precautions": info.get("precautions")
        })

    results.sort(
    key=lambda x: x["confidence"],
    reverse=True
)

    return results[:3]