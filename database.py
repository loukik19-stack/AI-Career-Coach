from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = "sqlite:///careerai.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ============================================================
# USER
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    resumes = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    job_targets = relationship(
        "JobTarget",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    interview_sessions = relationship(
        "InterviewSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ============================================================
# RESUME
# ============================================================

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title = Column(String(200), nullable=False)

    file_name = Column(String(255), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="resumes",
    )

    versions = relationship(
        "ResumeVersion",
        back_populates="resume",
        cascade="all, delete-orphan",
    )


# ============================================================
# RESUME VERSION
# ============================================================

class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False,
    )

    version_number = Column(
        Integer,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    match_score = Column(
        Float,
        nullable=True,
    )

    ats_score = Column(
        Float,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    is_current = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="versions",
    )


# ============================================================
# JOB TARGET
# ============================================================

class JobTarget(Base):
    __tablename__ = "job_targets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    role_title = Column(
        String(200),
        nullable=False,
    )

    company_name = Column(
        String(200),
        nullable=True,
    )

    job_description = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="job_targets",
    )


# ============================================================
# RESUME ANALYSIS
# ============================================================

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)

    resume_version_id = Column(
        Integer,
        ForeignKey("resume_versions.id"),
        nullable=False,
    )

    job_target_id = Column(
        Integer,
        ForeignKey("job_targets.id"),
        nullable=False,
    )

    match_score = Column(
        Float,
        nullable=True,
    )

    ats_score = Column(
        Float,
        nullable=True,
    )

    matched_skills = Column(
        Text,
        nullable=True,
    )

    missing_skills = Column(
        Text,
        nullable=True,
    )

    weak_skills = Column(
        Text,
        nullable=True,
    )

    experience_gaps = Column(
        Text,
        nullable=True,
    )

    ats_keywords = Column(
        Text,
        nullable=True,
    )

    resume_improvements = Column(
        Text,
        nullable=True,
    )

    high_priority_actions = Column(
        Text,
        nullable=True,
    )

    overall_assessment = Column(
        Text,
        nullable=True,
    )

    rewrite_suggestions = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# INTERVIEW SESSION
# ============================================================

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    role = Column(
        String(200),
        nullable=False,
    )

    interview_type = Column(
        String(50),
        nullable=False,
    )

    difficulty = Column(
        String(50),
        nullable=False,
    )

    overall_score = Column(
        Float,
        nullable=True,
    )

    technical_score = Column(
        Float,
        nullable=True,
    )

    communication_score = Column(
        Float,
        nullable=True,
    )

    clarity_score = Column(
        Float,
        nullable=True,
    )

    confidence_score = Column(
        Float,
        nullable=True,
    )

    completed = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="interview_sessions",
    )

    answers = relationship(
        "InterviewAnswer",
        back_populates="session",
        cascade="all, delete-orphan",
    )


# ============================================================
# INTERVIEW ANSWER
# ============================================================

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False,
    )

    question_number = Column(
        Integer,
        nullable=False,
    )

    question = Column(
        Text,
        nullable=False,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    score = Column(
        Float,
        nullable=True,
    )

    technical_score = Column(
        Float,
        nullable=True,
    )

    relevance_score = Column(
        Float,
        nullable=True,
    )

    structure_score = Column(
        Float,
        nullable=True,
    )

    clarity_score = Column(
        Float,
        nullable=True,
    )

    confidence_score = Column(
        Float,
        nullable=True,
    )

    strengths = Column(
        Text,
        nullable=True,
    )

    weaknesses = Column(
        Text,
        nullable=True,
    )

    feedback = Column(
        Text,
        nullable=True,
    )

    is_follow_up = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    session = relationship(
        "InterviewSession",
        back_populates="answers",
    )


# ============================================================
# CREATE DATABASE
# ============================================================

def init_database():
    """
    Create all database tables if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)


# ============================================================
# DATABASE SESSION HELPER
# ============================================================

def get_db():
    """
    Create a database session.

    Usage:

        db = get_db()

        try:
            # database operations
            pass
        finally:
            db.close()
    """
    return SessionLocal()


# ============================================================
# INITIALIZE DATABASE WHEN MODULE IS RUN
# ============================================================

if __name__ == "__main__":
    init_database()
    print("CareerAI database initialized successfully.")