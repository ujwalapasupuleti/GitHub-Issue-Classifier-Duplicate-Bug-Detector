import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "cleaned_issues.csv"

MODEL_PATH = BASE_DIR / "models"

MODEL_PATH.mkdir(exist_ok=True)


# Load dataset
print("Loading GitHub issues dataset...")

df = pd.read_csv(DATASET_PATH)

df = df.dropna(subset=["cleaned_text", "category"])

X = df["cleaned_text"]
y = df["category"]

print("Total records:", len(df))
print("\nCategories:")
print(y.value_counts())


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# TF-IDF vectorization
print("\nConverting text into numerical vectors...")

vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_vector = vectorizer.fit_transform(X_train)

X_test_vector = vectorizer.transform(X_test)


# Train classifier
print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_vector, y_train)


# Evaluation
predictions = model.predict(X_test_vector)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nMODEL EVALUATION")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# Save models
joblib.dump(
    model,
    MODEL_PATH / "issue_classifier.pkl"
)

joblib.dump(
    vectorizer,
    MODEL_PATH / "tfidf_vectorizer.pkl"
)


print("\nModel training completed!")

print("Models saved successfully.")