# GitHub Issue Classifier & Duplicate Bug Detector

An NLP-powered application that automatically classifies GitHub issues and identifies potentially duplicate bug reports using Machine Learning.

## Project Overview

Open-source repositories receive large numbers of issues every day. Manually reviewing and categorizing these issues can be time-consuming for developers and maintainers.

This project provides an automated solution that classifies GitHub issues into categories and identifies similar existing issues to help reduce duplicate reports.

## Key Features

- **Issue Classification:** Categorizes issues into Bug, Feature Request, and Documentation.
- **Duplicate Issue Detection:** Finds the top three most similar existing issues.
- **Text Processing:** Uses TF-IDF to convert issue text into numerical features.
- **Machine Learning:** Uses Logistic Regression for issue classification.
- **Similarity Matching:** Uses cosine similarity to identify potentially duplicate issues.
- **REST API:** Provides predictions through a FastAPI backend.
- **Interactive Dashboard:** Provides a Streamlit interface.
- **Automated Testing:** Uses Pytest to validate project functionality.
- **CI Pipeline:** Uses GitHub Actions to automatically run tests when code is pushed or a pull request is created.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Text Vectorization | TF-IDF |
| Classification | Logistic Regression |
| Similarity Detection | Cosine Similarity |
| Data Processing | Pandas, NumPy |
| Backend | FastAPI |
| Frontend | Streamlit |
| Model Storage | Joblib |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Version Control | Git and GitHub |
| Containerization Configuration | Docker |

## Project Architecture

1. GitHub issue data is collected using the GitHub API.
2. Issue titles and descriptions are preprocessed.
3. TF-IDF converts text into numerical feature vectors.
4. Logistic Regression predicts the issue category.
5. Cosine similarity compares the submitted issue with existing issues.
6. The system returns the predicted category and top three similar issues.
7. FastAPI provides the backend functionality.
8. Streamlit displays the results through an interactive dashboard.

## Project Structure

```text
github-issue-classifier/
│
├── backend/
│   ├── github_api.py
│   ├── analyze_dataset.py
│   ├── preprocessing.py
│   ├── classifier.py
│   ├── predict.py
│   ├── duplicate_detector.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── dataset/
│   ├── issues.csv
│   └── cleaned_issues.csv
│
├── models/
│   ├── issue_classifier.pkl
│   └── tfidf_vectorizer.pkl
│
├── tests/
│   └── test_classifier.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ujwalapasupuleti/GitHub-Issue-Classifier-Duplicate-Bug-Detector.git
```

### 2. Navigate to the project

```bash
cd GitHub-Issue-Classifier-Duplicate-Bug-Detector
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

### Start the Streamlit frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py
```

## Testing

Run the automated tests:

```bash
python -m pytest tests/ -v
```

The current test suite contains three tests covering model availability and prediction functionality.

**GitHub Actions CI:** Automatically installs project dependencies and executes the test suite after pushes and pull requests targeting the main branch.

## Future Enhancements

- Integrate transformer-based language models.
- Improve duplicate detection using semantic embeddings.
- Support additional GitHub repositories.
- Add issue priority and severity prediction.
- Deploy the application using a cloud platform.
- Introduce monitoring and performance analytics.

## Project Information

**Project Name:** GitHub Issue Classifier & Duplicate Bug Detector  
**Project ID:** NLP-46  
**Domain:** Natural Language Processing and Machine Learning  
**Developer:** Ujwala Pasupuleti

## License

This project is intended for educational and learning purposes. 
