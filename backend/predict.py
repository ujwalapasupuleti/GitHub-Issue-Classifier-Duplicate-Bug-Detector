import joblib

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models"


# Load saved models
model = joblib.load(
    MODEL_PATH / "issue_classifier.pkl"
)

vectorizer = joblib.load(
    MODEL_PATH / "tfidf_vectorizer.pkl"
)


def predict_issue(text):

    # Convert text into TF-IDF vectors
    vector = vectorizer.transform([text])

    # Predict category
    prediction = model.predict(vector)[0]

    # Calculate confidence
    probabilities = model.predict_proba(vector)[0]

    confidence = max(probabilities) * 100

    return {

        "category": prediction,

        "confidence": round(confidence, 2)

    }


if __name__ == "__main__":

    issue = input(
        "Enter GitHub issue description: "
    )

    result = predict_issue(issue)

    print("\nPredicted Category:", result["category"])

    print("Confidence:", result["confidence"], "%")