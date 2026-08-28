import streamlit as st


def progress_page():

    st.title("📊 Your Progress")

    st.write(
        "Track your resume and interview "
        "preparation over time."
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
            "Interviews Practiced",
            "0"
        )

    with col3:
        st.metric(
            "Average Confidence",
            "—"
        )

    st.divider()

    st.subheader("🎯 Preparation Goals")

    st.progress(0)

    st.write(
        "Complete your first resume analysis "
        "to begin tracking progress."
    )