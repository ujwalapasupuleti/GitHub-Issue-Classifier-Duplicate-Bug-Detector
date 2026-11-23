from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models"

def test_classifier_model_exists():
    assert (MODEL_PATH / "issue_classifier.pkl").exists()

def test_vectorizer_exists():
    assert (MODEL_PATH / "tfidf_vectorizer.pkl").exists()

def test_prediction():
    model = joblib.load(MODEL_PATH / "issue_classifier.pkl")
    vectorizer = joblib.load(MODEL_PATH / "tfidf_vectorizer.pkl")

    text = ["Application crashes during login"]
    vector = vectorizer.transform(text)
    prediction = model.predict(vector)

    assert prediction[0] in [
        "Bug",
        "Feature Request",
        "Documentation"
    ]
