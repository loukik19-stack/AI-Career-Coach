import streamlit as st

from resume_parser import extract_text_from_pdf


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🎯 AI Career Coach")

st.write(
    "Your AI-powered assistant for resumes, "
    "job matching, and interview preparation."
)

st.divider()


# -----------------------------
# RESUME ANALYZER
# -----------------------------

st.header("📄 Resume Analyzer")

st.write(
    "Upload your resume in PDF format."
)


# PDF uploader

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf"]
)


# -----------------------------
# WHEN A FILE IS UPLOADED
# -----------------------------

if uploaded_file is not None:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )

    # Button to read the resume

    if st.button("📖 Extract Resume Text"):

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

        st.subheader("📋 Extracted Resume")

        st.text_area(
            "Resume Text",
            resume_text,
            height=500
        )