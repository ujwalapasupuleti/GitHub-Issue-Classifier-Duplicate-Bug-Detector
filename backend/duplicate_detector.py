import pandas as pd
import joblib

from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "cleaned_issues.csv"

MODEL_PATH = BASE_DIR / "models"


# Load dataset
df = pd.read_csv(DATASET_PATH)

df = df.dropna(subset=["cleaned_text"])

# Load trained TF-IDF vectorizer
vectorizer = joblib.load(
    MODEL_PATH / "tfidf_vectorizer.pkl"
)


# Convert existing issues into vectors
issue_vectors = vectorizer.transform(
    df["cleaned_text"].astype(str)
)


def find_similar_issues(title, description, top_k=3):

    query = title + " " + description

    # Convert new issue into vector
    query_vector = vectorizer.transform([query])

    # Calculate cosine similarity
    similarities = cosine_similarity(
        query_vector,
        issue_vectors
    )[0]

    # Find top matching issues
    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:

        issue = df.iloc[index]

        results.append({

            "title": issue["title"],

            "category": issue["category"],

            "repository": issue["repository"],

            "similarity": round(
                similarities[index] * 100, 2
            ),

            "url": issue["url"]

        })

    return results


# Test application
if __name__ == "__main__":

    title = "Application crashes during login"

    description = (
        "The application stops working "
        "when users enter their login credentials."
    )

    results = find_similar_issues(
        title,
        description
    )

    print("\nTOP 3 SIMILAR GITHUB ISSUES")

    for i, issue in enumerate(results, 1):

        print(f"\nMatch {i}")

        print("Title:", issue["title"])

        print("Category:", issue["category"])

        print("Similarity:", issue["similarity"], "%")

        print("Repository:", issue["repository"])

        print("URL:", issue["url"])