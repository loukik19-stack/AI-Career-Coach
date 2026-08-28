import streamlit as st

from resume_parser import extract_text_from_pdf
from ai_engine import ask_ai


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎯",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .score-card {
        padding: 25px;
        border-radius: 15px;
        background-color: #f5f7fa;
        text-align: center;
    }

    .score-number {
        font-size: 40px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎯 CareerAI")

st.sidebar.write(
    "AI Career Preparation Platform"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Resume Analyzer",
        "🎤 Mock Interview",
        "📊 Progress"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🎯 CareerAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your AI-powered resume and interview coach.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🚀 What can CareerAI do?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            ### 📄 Resume Analysis

            Analyze your resume against
            a specific job description.

            Identify skill gaps and
            improve ATS compatibility.
            """
        )

    with col2:

        st.info(
            """
            ### 🎤 Mock Interviews

            Practice technical and
            behavioral interviews.

            Get structured AI feedback
            on your answers.
            """
        )

    with col3:

        st.info(
            """
            ### 📊 Progress Tracking

            Track your preparation,
            interview scores and
            improvement over time.
            """
        )

    st.divider()

    st.subheader("💡 How it works")

    st.write(
        """
        **1. Upload your resume**

        **2. Paste the job description**

        **3. CareerAI analyzes the match**

        **4. Identify your skill gaps**

        **5. Practice an adaptive interview**

        **6. Track your improvement**
        """
    )


# ==========================================
# RESUME ANALYZER
# ==========================================

elif page == "📄 Resume Analyzer":

    st.title("📄 Resume Intelligence")

    st.write(
        "Compare your resume against a target job."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )

    job_description = st.text_area(
        "💼 Job Description",
        height=250,
        placeholder=(
            "Paste the complete job description here..."
        )
    )

    if uploaded_file:

        st.success(
            f"Resume uploaded: {uploaded_file.name}"
        )

    if st.button(
        "🤖 Analyze Resume",
        type="primary"
    ):

        if not uploaded_file:

            st.warning(
                "Please upload your resume."
            )

        elif not job_description.strip():

            st.warning(
                "Please paste the job description."
            )

        else:

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            prompt = f"""
You are an expert recruitment and career coach.

Analyze this resume against the job description.

Do NOT invent information about the candidate.

RESUME:

{resume_text}

JOB DESCRIPTION:

{job_description}

Provide:

1. Resume-JD Match Score from 0-100

2. ATS Compatibility Score from 0-100

3. Strongly Matched Skills

4. Missing Skills

5. Weak Skills

6. Experience Gaps

7. Important ATS Keywords

8. Three Resume Improvements

9. Three Highest Priority Actions

10. A short overall assessment.

Use clear headings and bullet points.
"""

            with st.spinner(
                "🤖 AI is analyzing your resume..."
            ):

                result = ask_ai(prompt)

            st.divider()

            st.header("🧠 AI Analysis")

            st.write(result)


# ==========================================
# MOCK INTERVIEW
# ==========================================

elif page == "🎤 Mock Interview":

    st.title("🎤 AI Mock Interview")

    st.write(
        "Practice realistic interview questions."
    )

    st.divider()

    role = st.selectbox(
        "Target Role",
        [
            "Software Engineer",
            "Data Analyst",
            "Web Developer",
            "AI / ML Engineer",
            "General HR"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.info(
        f"Target: {role} | Level: {difficulty}"
    )

    st.subheader("Interview Question")

    st.write(
        "Tell me about yourself and why you "
        "are interested in this role."
    )

    answer = st.text_area(
        "Your answer",
        height=200,
        placeholder="Type your answer here..."
    )

    if st.button(
        "Evaluate Answer",
        type="primary"
    ):

        if not answer.strip():

            st.warning(
                "Please enter an answer."
            )

        else:

            prompt = f"""
You are an expert interview coach.

Evaluate this candidate's interview answer.

ROLE:
{role}

DIFFICULTY:
{difficulty}

QUESTION:
Tell me about yourself and why you
are interested in this role.

ANSWER:
{answer}

Evaluate:

1. Relevance
2. Clarity
3. Confidence
4. Structure
5. Communication
6. Overall score from 0-100
7. What was done well
8. What should improve
9. A better answer structure

Do not invent facts about the candidate.
"""

            with st.spinner(
                "🤖 Evaluating your answer..."
            ):

                feedback = ask_ai(prompt)

            st.divider()

            st.header("📊 Interview Feedback")

            st.write(feedback)


# ==========================================
# PROGRESS
# ==========================================

elif page == "📊 Progress":

    st.title("📊 Preparation Progress")

    st.write(
        "Track your career preparation journey."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Resume Score",
            "—"
        )

    with col2:

        st.metric(
            "Interviews",
            "0"
        )

    with col3:

        st.metric(
            "Average Score",
            "—"
        )

    st.divider()

    st.subheader("🎯 Preparation Roadmap")

    st.write(
        """
        ⬜ Upload your first resume

        ⬜ Analyze your resume

        ⬜ Identify skill gaps

        ⬜ Practice first interview

        ⬜ Improve weak areas

        ⬜ Practice again
        """
    )