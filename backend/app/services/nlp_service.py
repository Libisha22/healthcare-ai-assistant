import re

KNOWN_SYMPTOMS = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "nausea",
    "sneezing",
    "chest pain",
    "loss of smell"
]

def extract_symptoms(text: str):

    text = text.lower()

    found = []

    for symptom in KNOWN_SYMPTOMS:
        if symptom in text:
            found.append(symptom)

    return found