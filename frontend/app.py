import streamlit as st
import requests

st.set_page_config(
    page_title="GitHub Issue Detector",
    page_icon="🐛",
    layout="wide"
)

st.title("🐛 GitHub Issue Classifier")
st.subheader("AI-Powered Duplicate Bug Detection System")

st.write(
    "Automatically classify GitHub issues "
    "and identify similar previously reported problems."
)

st.divider()

st.header("Submit Your Issue")

title = st.text_input(
    "Issue Title",
    placeholder="Example: Login page crashes"
)

description = st.text_area(
    "Issue Description",
    height=150,
    placeholder="Describe the problem..."
)

if st.button("Analyze Issue", type="primary"):

    if not title.strip() or not description.strip():

        st.warning("Please enter both title and description.")

    else:

        with st.spinner("Analyzing your issue..."):

            try:

                response = requests.post(
                  "http://backend:8000/analyze",
                    json={
                        "title": title,
                        "description": description
                    },
                    timeout=60
                )

                response.raise_for_status()

                result = response.json()

                st.success("Analysis completed!")

                st.divider()

                st.header("Classification Result")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Predicted Category",
                        result["predicted_category"]
                    )

                with col2:
                    st.metric(
                        "Confidence",
                        f'{result["confidence"]}%'
                    )

                st.divider()

                st.header("Top 3 Similar GitHub Issues")

                for i, issue in enumerate(
                    result["similar_issues"], 1
                ):

                    with st.container(border=True):

                        st.subheader(
                            f'{i}. {issue["title"]}'
                        )

                        st.write(
                            f'Category: {issue["category"]}'
                        )

                        st.write(
                            f'Repository: {issue["repository"]}'
                        )

                        st.progress(
                            min(issue["similarity"] / 100, 1.0)
                        )

                        st.write(
                            f'Similarity: {issue["similarity"]}%'
                        )

                        st.link_button(
                            "View GitHub Issue",
                            issue["url"]
                        )

            except requests.exceptions.RequestException as error:

                st.error(f"API connection failed: {error}")

st.divider()

    