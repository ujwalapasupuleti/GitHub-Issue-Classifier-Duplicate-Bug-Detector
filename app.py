import streamlit as st

st.set_page_config(
    page_title="GitHub Issue Classifier",
    page_icon="🐛",
    layout="wide"
)

st.title("🐛 GitHub Issue Classifier")
st.subheader("AI-Powered Duplicate Bug Detection System")

st.write(
    "Automatically classify GitHub issues "
    "and identify previously reported problems."
)

st.divider()

st.header("Submit a GitHub Issue")

issue_title = st.text_input("Issue Title")

issue_description = st.text_area(
    "Issue Description",
    height=180,
    placeholder="Describe the issue here..."
)

if st.button("Analyze Issue"):

    if issue_title and issue_description:

        st.success("Issue submitted successfully!")

        st.write("### Submitted Issue")
        st.write("**Title:**", issue_title)
        st.write("**Description:**", issue_description)

        st.info(
            "AI classification and duplicate detection "
            "will be integrated in the next development phases."
        )

    else:
        st.warning("Please enter both title and description.")

st.divider()

st.caption("NLP-46 | GitHub Issue Classifier & Duplicate Bug Detector")