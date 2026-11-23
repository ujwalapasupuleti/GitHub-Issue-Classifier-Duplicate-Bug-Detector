import pandas as pd
import re
import html
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "dataset" / "issues.csv"

OUTPUT_FILE = BASE_DIR / "dataset" / "cleaned_issues.csv"


# Text cleaning function
def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Decode HTML entities
    text = html.unescape(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove markdown code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Remove markdown formatting
    text = re.sub(r'[#*_`~]', '', text)

    # Remove special characters
    text = re.sub(r'[^a-z0-9\s.,!?-]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# Dataset preprocessing
def preprocess_dataset():

    print("Loading GitHub dataset...")

    df = pd.read_csv(INPUT_FILE)

    print("Original records:", len(df))

    # Handle missing values
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")

    # Combine title and description
    df["text"] = (
        df["title"] + " " + df["description"]
    )

    # Clean issue text
    df["cleaned_text"] = df["text"].apply(clean_text)

    # Remove empty records
    df = df[df["cleaned_text"].str.len() > 0]

    # Remove duplicate issues
    df = df.drop_duplicates(subset=["repository", "issue_id"])

    # Remove duplicate text
    df = df.drop_duplicates(subset=["cleaned_text"])

    # Save processed dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nPreprocessing completed!")

    print("Cleaned records:", len(df))

    print("\nCategory distribution:")
    print(df["category"].value_counts())

    print("\nSample cleaned text:")
    print(df["cleaned_text"].head())


if __name__ == "__main__":
    preprocess_dataset()