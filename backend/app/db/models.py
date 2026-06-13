"""
backend/app/db/models.py

Defines the 7 Postgres tables for the Verified Research Agent as SQLAlchemy ORM
classes. Every class inherits from `Base` (defined in session.py), which is how
SQLAlchemy collects all table definitions into one registry so it can create them.

Schema relationships (one-to-many shown as parent --< child):
    papers        --< chunks
    research_jobs --< research_results
    research_jobs --< claims
    claims        --< evidence
    chunks        --< evidence
    research_jobs --< feedback

Column type notes:
    Integer       -> whole number, used for auto-increment primary keys
    String(n)     -> short text with a length cap (titles, labels, statuses)
    Text          -> unbounded text (chunk bodies, full answers, claim text)
    Float         -> decimal numbers (support scores, rates)
    DateTime      -> timestamps
    ForeignKey    -> a column whose value must match a primary key in another table
"""

from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


# ---------------------------------------------------------------------------
# 1. papers — metadata for every paper we ingest
# ---------------------------------------------------------------------------
class Paper(Base):
    __tablename__ = "papers"

    # primary_key=True makes this the unique row id; it auto-increments.
    paper_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(512))
    # nullable=True means the field is allowed to be empty (not every paper
    # we ingest will have clean authors/year/source metadata).
    authors: Mapped[str | None] = mapped_column(String(512), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str | None] = mapped_column(String(64), nullable=True)   # "arxiv", "pubmed", "upload"
    pdf_path: Mapped[str | None] = mapped_column(String(512), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relationship() is NOT a column. It is a Python-side convenience that lets
    # you write paper.chunks to get all child chunks, instead of writing a join
    # query by hand. back_populates wires the two sides together.
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="paper")


# ---------------------------------------------------------------------------
# 2. chunks — the text pieces a paper is split into, linked to a Qdrant vector
# ---------------------------------------------------------------------------
class Chunk(Base):
    __tablename__ = "chunks"

    chunk_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # ForeignKey ties this chunk to one row in papers. If papers.paper_id = 5,
    # a chunk with paper_id = 5 belongs to that paper.
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.paper_id"))

    section: Mapped[str | None] = mapped_column(String(128), nullable=True)  # "abstract", "methods", etc.
    text: Mapped[str] = mapped_column(Text)

    # The id of the matching vector stored in Qdrant. Postgres holds the human
    # metadata; Qdrant holds the embedding. This column is the bridge between them.
    qdrant_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    paper: Mapped["Paper"] = relationship(back_populates="chunks")
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="chunk")


# ---------------------------------------------------------------------------
# 3. research_jobs — one async research request (the unit of work)
# ---------------------------------------------------------------------------
class ResearchJob(Base):
    __tablename__ = "research_jobs"

    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    question: Mapped[str] = mapped_column(Text)
    # status moves through: "pending" -> "running" -> "completed" / "failed".
    status: Mapped[str] = mapped_column(String(32), default="pending")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # One job has exactly one result, but many claims and feedback rows.
    result: Mapped["ResearchResult"] = relationship(back_populates="job")
    claims: Mapped[list["Claim"]] = relationship(back_populates="job")
    feedback: Mapped[list["Feedback"]] = relationship(back_populates="job")


# ---------------------------------------------------------------------------
# 4. research_results — the final answer + quality metrics for a job
# ---------------------------------------------------------------------------
class ResearchResult(Base):
    __tablename__ = "research_results"

    # Here the primary key is also the foreign key: each result row corresponds
    # to exactly one job, so we reuse job_id as the id. This enforces one-result-
    # per-job at the database level.
    job_id: Mapped[int] = mapped_column(ForeignKey("research_jobs.job_id"), primary_key=True)

    answer: Mapped[str] = mapped_column(Text)
    grounding_score: Mapped[float | None] = mapped_column(Float, nullable=True)    # overall answer grounding
    unsupported_rate: Mapped[float | None] = mapped_column(Float, nullable=True)   # the headline ML metric

    job: Mapped["ResearchJob"] = relationship(back_populates="result")


# ---------------------------------------------------------------------------
# 5. claims — atomic claims extracted from an answer, each with a support score
# ---------------------------------------------------------------------------
class Claim(Base):
    __tablename__ = "claims"

    claim_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("research_jobs.job_id"))

    claim_text: Mapped[str] = mapped_column(Text)
    support_score: Mapped[float | None] = mapped_column(Float, nullable=True)   # S2+S4 fusion score, 0..1
    label: Mapped[str | None] = mapped_column(String(32), nullable=True)        # "Supported"/"Weak"/"Unsupported"

    job: Mapped["ResearchJob"] = relationship(back_populates="claims")
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="claim")


# ---------------------------------------------------------------------------
# 6. evidence — the chunk(s) used as evidence for a claim
# ---------------------------------------------------------------------------
class Evidence(Base):
    __tablename__ = "evidence"

    evidence_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # This row links a claim to the chunk that was used to verify it.
    claim_id: Mapped[int] = mapped_column(ForeignKey("claims.claim_id"))
    chunk_id: Mapped[int] = mapped_column(ForeignKey("chunks.chunk_id"))

    evidence_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_title: Mapped[str | None] = mapped_column(String(512), nullable=True)

    claim: Mapped["Claim"] = relationship(back_populates="evidence")
    chunk: Mapped["Chunk"] = relationship(back_populates="evidence")


# ---------------------------------------------------------------------------
# 7. feedback — optional user feedback on an answer or a specific claim
# ---------------------------------------------------------------------------
class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("research_jobs.job_id"))

    # claim_id is optional: feedback can be about the whole job OR one claim.
    claim_id: Mapped[int | None] = mapped_column(ForeignKey("claims.claim_id"), nullable=True)

    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)   # e.g. 1-5 or thumbs up/down as 1/0
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    job: Mapped["ResearchJob"] = relationship(back_populates="feedback")
