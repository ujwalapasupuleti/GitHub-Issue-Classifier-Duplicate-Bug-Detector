import requests
import pandas as pd
import os
import time

REPOSITORIES = [
    "streamlit/streamlit",
    "huggingface/transformers",
    "fastapi/fastapi",
    "pallets/flask",
    "django/django",
    "scikit-learn/scikit-learn"
]
def classify_label(labels):

    label_names = [
        label["name"].lower().replace("-", " ").replace("_", " ")
        for label in labels
    ]

    for label in label_names:

        if any(word in label for word in [
            "bug", "defect", "error", "crash"
        ]):
            return "Bug"

    for label in label_names:

        if any(word in label for word in [
            "documentation",
            "document",
            "docs",
            "doc"
        ]):
            return "Documentation"

    for label in label_names:

        if any(word in label for word in [
            "enhancement",
            "feature",
            "proposal"
        ]):
            return "Feature Request"

    return None


def collect_issues():

    all_issues = []

    headers = {
        "Accept": "application/vnd.github+json"
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    for repo in REPOSITORIES:

        print(f"Collecting issues from {repo}")

        url = f"https://api.github.com/repos/{repo}/issues"

        for page in range(1, 6):

            params = {
                "state": "all",
                "per_page": 100,
                "page": page
            }

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            issues = response.json()

            if not issues:
                break

            for issue in issues:

                # Exclude pull requests
                if "pull_request" in issue:
                    continue

                category = classify_label(
                    issue.get("labels", [])
                )

                if category is None:
                    continue

                all_issues.append({

                    "issue_id": issue["id"],
                    "repository": repo,
                    "title": issue["title"],
                    "description": issue.get("body") or "",
                    "category": category,
                    "url": issue["html_url"],
                    "state": issue["state"],
                    "created_at": issue["created_at"]

                })

            time.sleep(1)

    return all_issues


if __name__ == "__main__":

    issues = collect_issues()

    os.makedirs("dataset", exist_ok=True)

    df = pd.DataFrame(issues)

    if not df.empty:

        df.to_csv(
            "dataset/issues.csv",
            index=False
        )

        print("\nDataset collected successfully!")

        print("Total issues:", len(df))

        print("\nCategory distribution:")
        print(df["category"].value_counts())

    else:

        print("No labelled issues found.")