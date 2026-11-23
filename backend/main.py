from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import joblib

from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(
    title="GitHub Issue Classifier API",
    description="AI-powered issue classification and duplicate detection",
    version="1.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models"
DATASET_PATH = BASE_DIR / "dataset" / "cleaned_issues.csv"

# Load trained models
classifier = joblib.load(
    MODEL_PATH / "issue_classifier.pkl"
)

vectorizer = joblib.load(
    MODEL_PATH / "tfidf_vectorizer.pkl"
)

df = pd.read_csv(DATASET_PATH)

df = df.dropna(subset=["cleaned_text"])

issue_vectors = vectorizer.transform(
    df["cleaned_text"].astype(str)
)


class IssueRequest(BaseModel):
    title: str
    description: str


@app.get("/")
def home():
    return {
        "message": "GitHub Issue Classifier API is running",
        "status": "Active"
    }


@app.post("/analyze")
def analyze_issue(issue: IssueRequest):

    text = (
        issue.title + " " + issue.description
    ).strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Issue text cannot be empty"
        )

    vector = vectorizer.transform([text])

    category = classifier.predict(vector)[0]

    probabilities = classifier.predict_proba(vector)[0]

    confidence = max(probabilities) * 100

    similarities = cosine_similarity(
        vector,
        issue_vectors
    )[0]

    top_indices = similarities.argsort()[::-1][:3]

    similar_issues = []

    for index in top_indices:

        row = df.iloc[index]

        similar_issues.append({
            "title": str(row["title"]),
            "category": str(row["category"]),
            "repository": str(row["repository"]),
            "similarity": round(
                float(similarities[index] * 100), 2
            ),
            "url": str(row["url"])
        })

    return {
        "predicted_category": str(category),
        "confidence": round(float(confidence), 2),
        "similar_issues": similar_issues
    }
app = FastAPI(
    title="GitHub Issue Classifier API",
    description="AI-powered issue classification and duplicate detection",
    version="1.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models"
DATASET_PATH = BASE_DIR / "dataset" / "cleaned_issues.csv"

# Load trained models
try:
    classifier = joblib.load(
        MODEL_PATH / "issue_classifier.pkl"
    )

    vectorizer = joblib.load(
        MODEL_PATH / "tfidf_vectorizer.pkl"
    )

    df = pd.read_csv(DATASET_PATH)

    df = df.dropna(subset=["cleaned_text"])

    issue_vectors = vectorizer.transform(
        df["cleaned_text"].astype(str)
    )

except Exception as error:
    raise RuntimeError(
        f"Could not load project resources: {error}"
    )


class IssueRequest(BaseModel):
    title: str
    description: str


@app.get("/")
def home():
    return {
        "message": "GitHub Issue Classifier API is running",
        "status": "Active"
    }


@app.post("/analyze")
def analyze_issue(issue: IssueRequest):

    text = (
        issue.title + " " + issue.description
    ).strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Issue text cannot be empty"
        )

    # Classification
    vector = vectorizer.transform([text])

    category = classifier.predict(vector)[0]

    probabilities = classifier.predict_proba(vector)[0]

    confidence = max(probabilities) * 100

    # Duplicate detection
    similarities = cosine_similarity(
        vector,
        issue_vectors
    )[0]

    top_indices = similarities.argsort()[::-1][:3]

    similar_issues = []

    for index in top_indices:

        row = df.iloc[index]

        similar_issues.append({
            "title": str(row["title"]),
            "category": str(row["category"]),
            "repository": str(row["repository"]),
            "similarity": round(
                float(similarities[index] * 100), 2
            ),
            "url": str(row["url"])
        })

    return {
        "predicted_category": str(category),
        "confidence": round(float(confidence), 2),
        "similar_issues": similar_issues
    }
