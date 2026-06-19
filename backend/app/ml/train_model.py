import os
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# =========================
# 1. FIXED PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "app", "ml", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "app", "ml", "vectorizer.pkl")

print("\nDATA PATH:", DATA_PATH)

# Safety check
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset NOT found at: {DATA_PATH}")

# =========================
# 2. LOAD DATA
# =========================
df = pd.read_csv(DATA_PATH)
df = df.dropna()

print("\nDataset Shape:", df.shape)
print("Unique diseases:", df["disease"].nunique())

X = df["symptoms"]
y = df["disease"]

# =========================
# 3. VECTORIZE TEXT (IMPROVED NLP)
# =========================
vectorizer = TfidfVectorizer(stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

# =========================
# 4. TRAIN-TEST SPLIT (SAFE)
# =========================
try:
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
except ValueError:
    print("\n⚠ Stratify failed → using normal split")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized,
        y,
        test_size=0.2,
        random_state=42
    )

# =========================
# 5. MODEL TRAINING
# =========================
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# =========================
# 6. PREDICTION
# =========================
predictions = model.predict(X_test)

# =========================
# 7. EVALUATION
# =========================
print("\n===== MODEL EVALUATION =====")

print("Accuracy :", round(accuracy_score(y_test, predictions), 2))
print("Precision:", round(precision_score(y_test, predictions, average="weighted", zero_division=0), 2))
print("Recall   :", round(recall_score(y_test, predictions, average="weighted", zero_division=0), 2))
print("F1 Score :", round(f1_score(y_test, predictions, average="weighted", zero_division=0), 2))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# =========================
# 8. FINAL TRAINING (FULL DATA)
# =========================
model.fit(X_vectorized, y)

# =========================
# 9. SAVE MODEL
# =========================
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

print("\n✅ Model trained and saved successfully!")