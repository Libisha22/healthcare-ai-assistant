import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv("data/training_data.csv")

X = df["symptoms"]
y = df["disease"]

vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

model = MultinomialNB()

model.fit(X_vectorized, y)

with open("app/ml/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("app/ml/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model trained successfully!")