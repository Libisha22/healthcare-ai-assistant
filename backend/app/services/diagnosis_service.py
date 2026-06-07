import pandas as pd
from app.services.nlp_service import extract_symptoms

df = pd.read_csv("data/disease_dataset.csv")

def analyze_symptom(symptom: str):

    extracted = extract_symptoms(symptom)
    symptom = " ".join(extracted).lower()

    results = []

    for _, row in df.iterrows():

        disease = row["Disease"]

        symptoms = row["Symptoms"].lower().split(";")

        score = 0

        for s in symptoms:
            if s in symptom:
                score += 1

        if score > 0:

            confidence = round(
                score / len(symptoms),
                2
            )

            results.append({
                "condition": disease,
                "confidence": confidence
            })

    if not results:

        results.append({
            "condition": "Unknown Condition",
            "confidence": 0.10
        })

    return results