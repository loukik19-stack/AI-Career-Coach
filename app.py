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
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .score-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f5f7fa;
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    .score-number {
        font-size: 38px;
        font-weight: 700;
    }

    .section-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎯 CareerAI")

st.sidebar.caption(
    "AI-Powered Resume & Interview Coach"
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

    st.subheader("🚀 Career Preparation Suite")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            ### 📄 Resume Intelligence

            Upload your resume and compare it
            against a target job description.

            **Identify:**
            - Match score
            - ATS compatibility
            - Skill gaps
            - Missing keywords
            - Improvement opportunities
            """
        )

    with col2:

        st.info(
            """
            ### 🎤 AI Mock Interview

            Practice realistic technical and
            behavioral interview questions.

            **Get feedback on:**
            - Relevance
            - Clarity
            - Structure
            - Confidence
            """
        )

    with col3:

        st.info(
            """
            ### 📊 Progress Tracking

            Track your preparation journey.

            **Monitor:**
            - Resume performance
            - Interview attempts
            - Average scores
            - Improvement areas
            """
        )

    st.divider()

    st.subheader("💡 How CareerAI Works")

    steps = st.columns(5)

    with steps[0]:
        st.markdown("### 1️⃣")
        st.write("Upload Resume")

    with steps[1]:
        st.markdown("### 2️⃣")
        st.write("Add Job Description")

    with steps[2]:
        st.markdown("### 3️⃣")
        st.write("AI Analysis")

    with steps[3]:
        st.markdown("### 4️⃣")
        st.write("Practice Interview")

    with steps[4]:
        st.markdown("### 5️⃣")
        st.write("Track Progress")


# ==========================================
# RESUME ANALYZER
# ==========================================

elif page == "📄 Resume Analyzer":

    st.title("📄 Resume Intelligence")

    st.write(
        "Analyze how well your resume matches a target job "
        "and discover exactly what you should improve."
    )

    st.divider()

    # --------------------------------------
    # INPUTS
    # --------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📄 Your Resume")

        uploaded_file = st.file_uploader(
            "Upload your resume as PDF",
            type=["pdf"]
        )

        if uploaded_file:

            st.success(
                f"✓ {uploaded_file.name} uploaded"
            )

    with col2:

        st.subheader("💼 Target Job")

        job_description = st.text_area(
            "Paste the complete job description",
            height=220,
            placeholder=(
                "Example:\n\n"
                "We are looking for a Python developer "
                "with experience in SQL, REST APIs, Git..."
            )
        )

    st.divider()

    # --------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------

    analyze_button = st.button(
        "🤖 Analyze Resume",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not uploaded_file:

            st.warning(
                "⚠️ Please upload your resume PDF first."
            )

        elif not job_description.strip():

            st.warning(
                "⚠️ Please paste the job description first."
            )

        else:

            # --------------------------------------
            # EXTRACT RESUME TEXT
            # --------------------------------------

            with st.spinner(
                "📄 Reading your resume..."
            ):

                resume_text = extract_text_from_pdf(
                    uploaded_file
                )

            if not resume_text.strip():

                st.error(
                    "Could not extract text from this PDF. "
                    "Please try another PDF."
                )

            else:

                # --------------------------------------
                # AI PROMPT
                # --------------------------------------

                prompt = f"""
You are an expert ATS resume analyst,
technical recruiter, and career coach.

Your job is to analyze a candidate's resume
against a target job description.

IMPORTANT RULES:

1. Do NOT invent candidate experience.
2. Do NOT claim the candidate has a skill
   unless it appears in the resume.
3. Distinguish clearly between:
   - skills the candidate already demonstrates
   - skills missing from the resume
   - skills that are weak or insufficiently demonstrated
4. Base every recommendation on the resume
   and job description.
5. Be concise but useful.

RESUME:

{resume_text}

TARGET JOB DESCRIPTION:

{job_description}

Provide the analysis using EXACTLY these headings:

MATCH SCORE:
Give a score from 0-100 representing how well
the resume matches the job.

ATS SCORE:
Give a score from 0-100 representing how well
the resume is optimized for ATS screening.

MATCHED SKILLS:
List important skills from the job description
that are clearly present in the resume.

MISSING SKILLS:
List important job requirements that are not
demonstrated in the resume.

WEAK SKILLS:
List skills that appear but are weak,
unclear, or insufficiently demonstrated.

EXPERIENCE GAPS:
Identify important experience requirements
that the resume does not demonstrate.

ATS KEYWORDS:
List important keywords from the job description
that should appear naturally in the resume.

RESUME IMPROVEMENTS:
Give exactly 5 specific improvements.

HIGH PRIORITY ACTIONS:
Give exactly 3 actions the candidate should
take first.

OVERALL ASSESSMENT:
Give a short professional assessment.

RESUME REWRITE SUGGESTIONS:
Provide 3 examples of how existing resume
bullet points could be rewritten to be clearer,
more specific, and achievement-oriented.

IMPORTANT:
Do not fabricate achievements, metrics,
technologies, job titles, or experience.
"""


                # --------------------------------------
                # GEMINI ANALYSIS
                # --------------------------------------

                with st.spinner(
                    "🤖 Gemini is analyzing your resume..."
                ):

                    result = ask_ai(prompt)

                # --------------------------------------
                # DISPLAY RESULTS
                # --------------------------------------

                st.divider()

                st.header("🧠 Resume Analysis")

                st.caption(
                    "AI-generated analysis based on your "
                    "resume and target job description."
                )

                st.write(result)

                st.divider()

                st.success(
                    "✅ Analysis complete. Use the feedback "
                    "to tailor your resume to this role."
                )


# ==========================================
# MOCK INTERVIEW
# ==========================================

elif page == "🎤 Mock Interview":

    st.title("🎤 AI Mock Interview")

    st.write(
        "Practice realistic interview questions "
        "and receive structured AI feedback."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

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

    with col2:

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

    st.info(
        f"🎯 Target Role: **{role}**  |  "
        f"Difficulty: **{difficulty}**"
    )

    st.subheader("💬 Interview Question")

    st.write(
        "**Tell me about yourself and why you "
        "are interested in this role.**"
    )

    answer = st.text_area(
        "Your answer",
        height=220,
        placeholder=(
            "Type your answer as if you were "
            "speaking to an interviewer..."
        )
    )

    if st.button(
        "🤖 Evaluate My Answer",
        type="primary",
        use_container_width=True
    ):

        if not answer.strip():

            st.warning(
                "⚠️ Please enter your answer first."
            )

        else:

            prompt = f"""
You are an expert interview coach.

Evaluate the candidate's answer fairly.

ROLE:
{role}

DIFFICULTY:
{difficulty}

QUESTION:
Tell me about yourself and why you are
interested in this role.

CANDIDATE ANSWER:
{answer}

Evaluate the answer on:

1. Relevance
2. Clarity
3. Confidence
4. Structure
5. Communication

Give each a score from 0-100.

Then provide:

OVERALL SCORE:
Give one score from 0-100.

WHAT WAS DONE WELL:
Give 3 specific strengths.

WHAT TO IMPROVE:
Give 3 specific improvements.

BETTER STRUCTURE:
Explain how the candidate could structure
this answer more effectively.

COACHING TIP:
Give one practical tip for the next attempt.

Do not invent facts about the candidate.
"""

            with st.spinner(
                "🤖 AI is evaluating your answer..."
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
        "Your preparation dashboard."
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