import pickle

with open("app/ml/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("app/ml/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def predict_disease(symptoms: str):

    transformed = vectorizer.transform([symptoms])

    prediction = model.predict(transformed)

    return prediction[0]