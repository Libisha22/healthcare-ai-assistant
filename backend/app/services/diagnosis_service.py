def analyze_symptom(symptom: str):

    symptom = symptom.lower()

    if "fever" in symptom:
        return ["Common Cold", "Flu"]

    elif "headache" in symptom:
        return ["Migraine", "Stress"]

    elif "cough" in symptom:
        return ["Viral Infection", "Bronchitis"]

    else:
        return ["Unknown Condition"]