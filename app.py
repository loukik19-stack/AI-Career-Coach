import streamlit as st

from resume_parser import extract_text_from_pdf
from ai_engine import ask_ai, ask_ai_json

# ==========================================
# INTERVIEW QUESTION BANK
# ==========================================

TECHNICAL_QUESTION_BANK = {
    "Software Engineer": [
        "Explain the difference between a stack and a queue.",
        "What is the time complexity of binary search?",
        "What is object-oriented programming?",
        "How would you debug a program that is producing incorrect output?",
        "Explain the difference between a process and a thread."
    ],

    "Data Analyst": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How would you handle missing data in a dataset?",
        "Explain the difference between mean and median.",
        "How would you identify an outlier in a dataset?",
        "What steps would you take when starting a new data analysis project?"
    ],

    "Web Developer": [
        "What is the difference between HTTP and HTTPS?",
        "Explain the difference between frontend and backend development.",
        "What is a REST API?",
        "What happens when you enter a URL into a browser?",
        "What is the difference between authentication and authorization?"
    ],

    "AI / ML Engineer": [
        "What is the difference between supervised and unsupervised learning?",
        "What is overfitting and how can it be reduced?",
        "Explain the purpose of a training and testing dataset.",
        "What is a neural network?",
        "How would you evaluate a machine learning model?"
    ]
}


BEHAVIORAL_QUESTION_BANK = [
    "Tell me about yourself.",
    "Why are you interested in this role?",
    "Tell me about a difficult problem you solved.",
    "Describe a time you worked as part of a team.",
    "Tell me about a mistake you made and what you learned from it.",
    "How do you handle disagreement with a teammate?",
    "Describe a situation where you had to learn something quickly.",
    "What are your greatest strengths?",
    "What is one area you are currently trying to improve?",
    "Where do you see yourself developing professionally?"
]
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
        margin-bottom: 25px;
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

            Analyze your resume against a
            target job description.

            **Discover:**
            - Resume match
            - ATS compatibility
            - Skill gaps
            - Keywords
            - Improvements
            """
        )

    with col2:

        st.info(
            """
            ### 🎤 AI Mock Interview

            Practice technical and behavioral
            interview questions.

            **Receive feedback on:**
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
            - Scores
            - Weak areas
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
        "Analyze your resume against a target job "
        "and identify exactly what you should improve."
    )

    st.divider()

    col1, col2 = st.columns(2)

    # --------------------------------------
    # RESUME INPUT
    # --------------------------------------

    with col1:

        st.subheader("📄 Resume")

        uploaded_file = st.file_uploader(
            "Upload your resume PDF",
            type=["pdf"]
        )

        if uploaded_file:

            st.success(
                f"✓ {uploaded_file.name}"
            )

    # --------------------------------------
    # JOB DESCRIPTION INPUT
    # --------------------------------------

    with col2:

        st.subheader("💼 Target Job")

        job_description = st.text_area(
            "Paste the job description",
            height=220,
            placeholder=(
                "Paste the complete job description here..."
            )
        )

    st.divider()

    # --------------------------------------
    # ANALYZE
    # --------------------------------------

    if st.button(
        "🤖 Analyze Resume",
        type="primary",
        use_container_width=True
    ):

        if not uploaded_file:

            st.warning(
                "⚠️ Please upload your resume PDF."
            )

        elif not job_description.strip():

            st.warning(
                "⚠️ Please paste the job description."
            )

        else:

            # Extract resume text

            with st.spinner(
                "📄 Reading resume..."
            ):

                resume_text = extract_text_from_pdf(
                    uploaded_file
                )

            if not resume_text.strip():

                st.error(
                    "Could not extract text from this PDF."
                )

            else:

                # --------------------------------------
                # STRUCTURED AI PROMPT
                # --------------------------------------

                prompt = f"""
You are an expert ATS resume analyst,
technical recruiter, and career coach.

Analyze the candidate's resume against
the target job description.

IMPORTANT RULES:

- Never invent candidate experience.
- Never invent skills.
- Never invent achievements.
- Base your analysis only on the supplied resume
  and job description.
- Distinguish between demonstrated skills,
  missing skills, and weakly demonstrated skills.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "match_score": 0,
    "ats_score": 0,

    "matched_skills": [],
    "missing_skills": [],
    "weak_skills": [],

    "experience_gaps": [],

    "ats_keywords": [],

    "resume_improvements": [],

    "high_priority_actions": [],

    "overall_assessment": "",

    "rewrite_suggestions": []
}}

SCORING:

match_score:
0-100 estimate of how well the resume matches
the target job.

ats_score:
0-100 estimate of ATS compatibility.

matched_skills:
Important job skills clearly demonstrated
in the resume.

missing_skills:
Important job skills not demonstrated
in the resume.

weak_skills:
Skills that appear but are weak,
unclear, or insufficiently demonstrated.

experience_gaps:
Important job requirements or experience
not demonstrated by the resume.

ats_keywords:
Important keywords from the job description
that could naturally be incorporated into
the resume when truthful.

resume_improvements:
Exactly 5 specific improvements.

high_priority_actions:
Exactly 3 actions.

overall_assessment:
A concise professional assessment.

rewrite_suggestions:
Exactly 3 examples of how existing resume
bullet points could be rewritten.

Do not fabricate information.

RESUME:

{resume_text}

JOB DESCRIPTION:

{job_description}
"""

                # --------------------------------------
                # GEMINI ANALYSIS
                # --------------------------------------

                with st.spinner(
                    "🤖 Gemini is analyzing your resume..."
                ):

                    analysis = ask_ai_json(prompt)

                # --------------------------------------
                # ERROR CHECK
                # --------------------------------------

                if "error" in analysis:

                    st.error(
                        "AI analysis failed."
                    )

                    st.code(
                        analysis["error"]
                    )

                else:

                    # ----------------------------------
                    # SCORE CARDS
                    # ----------------------------------

                    st.divider()

                    st.header("🎯 Resume Performance")

                    score1, score2 = st.columns(2)

                    with score1:

                        st.metric(
                            "Resume-JD Match",
                            f"{analysis.get('match_score', 0)}/100"
                        )

                    with score2:

                        st.metric(
                            "ATS Compatibility",
                            f"{analysis.get('ats_score', 0)}/100"
                        )

                    st.divider()

                    # ----------------------------------
                    # SKILLS
                    # ----------------------------------

                    skill1, skill2, skill3 = st.columns(3)

                    with skill1:

                        st.subheader("✅ Matched Skills")

                        matched = analysis.get(
                            "matched_skills",
                            []
                        )

                        if matched:

                            for skill in matched:

                                st.success(
                                    str(skill)
                                )

                        else:

                            st.write(
                                "No strong matches identified."
                            )

                    with skill2:

                        st.subheader("⚠️ Missing Skills")

                        missing = analysis.get(
                            "missing_skills",
                            []
                        )

                        if missing:

                            for skill in missing:

                                st.warning(
                                    str(skill)
                                )

                        else:

                            st.write(
                                "No major missing skills identified."
                            )

                    with skill3:

                        st.subheader("🟡 Weak Skills")

                        weak = analysis.get(
                            "weak_skills",
                            []
                        )

                        if weak:

                            for skill in weak:

                                st.info(
                                    str(skill)
                                )

                        else:

                            st.write(
                                "No major weak skills identified."
                            )

                    # ----------------------------------
                    # EXPERIENCE GAPS
                    # ----------------------------------

                    st.divider()

                    st.subheader(
                        "📌 Experience Gaps"
                    )

                    gaps = analysis.get(
                        "experience_gaps",
                        []
                    )

                    if gaps:

                        for gap in gaps:

                            st.write(
                                f"• {gap}"
                            )

                    else:

                        st.write(
                            "No significant experience gaps identified."
                        )

                    # ----------------------------------
                    # ATS KEYWORDS
                    # ----------------------------------

                    st.divider()

                    st.subheader(
                        "🔑 Important ATS Keywords"
                    )

                    keywords = analysis.get(
                        "ats_keywords",
                        []
                    )

                    if keywords:

                        st.write(
                            " • ".join(
                                str(keyword)
                                for keyword in keywords
                            )
                        )

                    else:

                        st.write(
                            "No additional keywords identified."
                        )

                    # ----------------------------------
                    # IMPROVEMENTS
                    # ----------------------------------

                    st.divider()

                    st.subheader(
                        "💡 Resume Improvements"
                    )

                    improvements = analysis.get(
                        "resume_improvements",
                        []
                    )

                    for index, improvement in enumerate(
                        improvements,
                        start=1
                    ):

                        st.write(
                            f"**{index}.** {improvement}"
                        )

                    # ----------------------------------
                    # HIGH PRIORITY ACTIONS
                    # ----------------------------------

                    st.divider()

                    st.subheader(
                        "🎯 High Priority Actions"
                    )

                    actions = analysis.get(
                        "high_priority_actions",
                        []
                    )

                    for index, action in enumerate(
                        actions,
                        start=1
                    ):

                        st.write(
                            f"**{index}.** {action}"
                        )

                    # ----------------------------------
                    # OVERALL ASSESSMENT
                    # ----------------------------------

                    st.divider()

                    st.subheader(
                        "🧠 Overall Assessment"
                    )

                    st.info(
                        analysis.get(
                            "overall_assessment",
                            "No assessment available."
                        )
                    )

                    # ----------------------------------
                    # REWRITE SUGGESTIONS
                    # ----------------------------------

                    st.divider()

                    st.subheader(
                        "✍️ Resume Rewrite Suggestions"
                    )

                    rewrites = analysis.get(
                        "rewrite_suggestions",
                        []
                    )

                    for index, rewrite in enumerate(
                        rewrites,
                        start=1
                    ):

                        st.write(
                            f"**Example {index}**"

                        )

                        st.info(
                            str(rewrite)
                        )
# ==========================================
# MOCK INTERVIEW
# ==========================================

elif page == "🎤 Mock Interview":

    st.title("🎤 AI Mock Interview")

    st.write(
        "Practice realistic, AI-generated interview questions "
        "and receive structured feedback."
    )

    st.divider()

    # --------------------------------------
    # INTERVIEW SETTINGS
    # --------------------------------------

    col1, col2, col3 = st.columns(3)

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

        interview_type = st.selectbox(
            "Interview Type",
            [
                "Technical",
                "Behavioral / HR",
                "Mixed"
            ]
        )

    with col3:

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

    st.info(
        f"🎯 **{role}** | "
        f"💬 **{interview_type}** | "
        f"📈 **{difficulty}**"
    )

    # --------------------------------------
    # GENERATE QUESTION
    # --------------------------------------

    if st.button(
        "🎲 Generate Interview Question",
        type="primary",
        use_container_width=True
    ):

        question_prompt = f"""
You are an expert technical recruiter and
interview coach.

Generate ONE realistic interview question.

TARGET ROLE:
{role}

INTERVIEW TYPE:
{interview_type}

DIFFICULTY:
{difficulty}

Rules:

- The question must be appropriate for the role.
- The question must match the selected interview type.
- The difficulty must match the selected level.
- Do not provide the answer.
- Do not provide explanations.
- Return ONLY the interview question.
"""

        with st.spinner(
            "🤖 Generating interview question..."
        ):

            generated_question = ask_ai(
                question_prompt
            )

        if generated_question.startswith(
            "AI Error:"
        ):

            st.error(
                generated_question
            )

        else:

            st.session_state.interview_question = (
                generated_question.strip()
            )

            st.session_state.interview_role = role

            st.session_state.interview_type = (
                interview_type
            )

            st.session_state.interview_difficulty = (
                difficulty
            )

    # --------------------------------------
    # DISPLAY GENERATED QUESTION
    # --------------------------------------

    if "interview_question" in st.session_state:

        st.divider()

        st.subheader(
            "💬 Interview Question"
        )

        st.info(
            st.session_state.interview_question
        )

        st.subheader(
            "✍️ Your Answer"
        )

        answer = st.text_area(
            "Answer the interviewer",
            height=220,
            placeholder=(
                "Type your answer as if you were "
                "speaking to an interviewer..."
            ),
            key="interview_answer"
        )

        # ----------------------------------
        # EVALUATE ANSWER
        # ----------------------------------

        if st.button(
            "🤖 Evaluate My Answer",
            type="primary",
            use_container_width=True
        ):

            if not answer.strip():

                st.warning(
                    "⚠️ Please enter an answer."
                )

            else:

                evaluation_prompt = f"""
You are an expert interview coach and recruiter.

Evaluate the candidate's answer objectively.

ROLE:
{st.session_state.interview_role}

INTERVIEW TYPE:
{st.session_state.interview_type}

DIFFICULTY:
{st.session_state.interview_difficulty}

QUESTION:
{st.session_state.interview_question}

CANDIDATE ANSWER:
{answer}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "relevance": 0,
    "clarity": 0,
    "confidence": 0,
    "structure": 0,
    "communication": 0,
    "overall_score": 0,
    "what_was_done_well": [],
    "what_to_improve": [],
    "better_answer_structure": "",
    "coaching_tip": ""
}}

SCORING:

relevance:
0-100. How directly the answer addresses the question.

clarity:
0-100. How clearly and understandably the candidate communicates.

confidence:
0-100. How confidently and decisively the answer is expressed
through the candidate's wording.

structure:
0-100. How logically and effectively the answer is organized.

communication:
0-100. Overall effectiveness and professionalism of the response.

overall_score:
0-100. Overall evaluation based on the five dimensions.

what_was_done_well:
Exactly 3 specific positive observations based only on the answer.

what_to_improve:
Exactly 3 specific and actionable improvements.

better_answer_structure:
A practical structure the candidate could use
to answer this question more effectively.

coaching_tip:
Exactly one practical interview coaching tip.

IMPORTANT:
- Do not invent facts about the candidate.
- Do not assume experience that is not stated.
- Evaluate only information contained in the answer.
- Be constructive and specific.
- Do not judge physical appearance.
- Return ONLY valid JSON.
"""

                with st.spinner(
                    "🤖 Evaluating your answer..."
                ):

                    feedback = ask_ai_json(evaluation_prompt)

st.divider()

st.header(
    "📊 Interview Feedback"
)

if "error" in feedback:

    st.error(
        "AI evaluation failed."
    )

    st.code(
        feedback["error"]
    )

else:

    score1, score2, score3, score4, score5 = st.columns(5)

    with score1:

        st.metric(
            "Relevance",
            f"{feedback.get('relevance', 0)}/100"
        )

    with score2:

        st.metric(
            "Clarity",
            f"{feedback.get('clarity', 0)}/100"
        )

    with score3:

        st.metric(
            "Confidence",
            f"{feedback.get('confidence', 0)}/100"
        )

    with score4:

        st.metric(
            "Structure",
            f"{feedback.get('structure', 0)}/100"
        )

    with score5:

        st.metric(
            "Communication",
            f"{feedback.get('communication', 0)}/100"
        )

    st.divider()

    st.subheader(
        "🏆 Overall Score"
    )

    st.metric(
        "Interview Performance",
        f"{feedback.get('overall_score', 0)}/100"
    )

    st.subheader(
        "✅ What Was Done Well"
    )

    for point in feedback.get(
        "what_was_done_well",
        []
    ):

        st.success(
            str(point)
        )

    st.subheader(
        "⚠️ What To Improve"
    )

    for point in feedback.get(
        "what_to_improve",
        []
    ):

        st.warning(
            str(point)
        )

    st.subheader(
        "🧠 Better Answer Structure"
    )

    st.info(
        feedback.get(
            "better_answer_structure",
            "No structure provided."
        )
    )

    st.subheader(
        "🎯 Coaching Tip"
    )

    st.info(
        feedback.get(
            "coaching_tip",
            "No coaching tip provided."
        )
    )
# ==========================================
# PROGRESS
# ==========================================

elif page == "📊 Progress":

    st.title(
        "📊 Preparation Progress"
    )

    st.write(
        "Your career preparation dashboard."
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

    st.subheader(
        "🎯 Preparation Roadmap"
    )

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