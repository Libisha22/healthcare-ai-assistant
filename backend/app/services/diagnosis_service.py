def analyze_symptom(symptom: str):

    symptom = symptom.lower()

    conditions = []

    if "fever" in symptom:

        conditions.append({
            "condition": "Flu",
            "confidence": 0.90
        })

        conditions.append({
            "condition": "Common Cold",
            "confidence": 0.75
        })

    if "cough" in symptom:

        conditions.append({
            "condition": "COVID-19",
            "confidence": 0.80
        })

        conditions.append({
            "condition": "Bronchitis",
            "confidence": 0.65
        })

    if "headache" in symptom:

        conditions.append({
            "condition": "Migraine",
            "confidence": 0.85
        })

        conditions.append({
            "condition": "Stress",
            "confidence": 0.70
        })

    if not conditions:

        conditions.append({
            "condition": "Unknown Condition",
            "confidence": 0.10
        })

    return conditions