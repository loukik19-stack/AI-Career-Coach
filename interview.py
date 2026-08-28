import streamlit as st


def interview_page():

    st.title("🎤 Mock Interview")

    st.write(
        "Practice realistic interview questions "
        "and receive structured feedback."
    )

    st.divider()

    role = st.selectbox(
        "Select interview type",
        [
            "Software Engineer",
            "Data Analyst",
            "Web Developer",
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
        f"Interview: {role} | Difficulty: {difficulty}"
    )

    st.subheader("Question")

    st.write(
        "Tell me about yourself and your "
        "most relevant experience."
    )

    answer = st.text_area(
        "Your answer",
        height=200,
        placeholder="Type your answer here..."
    )

    if st.button("Evaluate Answer"):

        if not answer.strip():

            st.warning(
                "Please enter an answer first."
            )

        else:

            st.success(
                "Answer received! AI evaluation "
                "will appear here."
            )

            st.subheader("📊 Feedback")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Clarity", "—")

            with col2:
                st.metric("Relevance", "—")

            with col3:
                st.metric("Confidence", "—")

            st.write(
                "AI feedback will be connected "
                "after the local AI is ready."
            )