"""Initial V1 persistence schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-24 21:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("preferences", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2. sessions
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=64), nullable=False),
        sa.Column("current_state", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])

    # 3. explanation_documents
    op.create_table(
        "explanation_documents",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=64), nullable=False),
        sa.Column("intent", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("document_json", sa.JSON(), nullable=False),
        sa.Column("validation_json", sa.JSON(), nullable=False),
        sa.Column("provider_metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_explanation_documents_session_id", "explanation_documents", ["session_id"])

    # 4. messages
    op.create_table(
        "messages",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("attachments", sa.JSON(), nullable=False),
        sa.Column("explanation_document_id", sa.String(length=64), sa.ForeignKey("explanation_documents.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_messages_session_id", "messages", ["session_id"])

    # 5. problems
    op.create_table(
        "problems",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_image", sa.String(length=1024), nullable=True),
        sa.Column("normalized_text", sa.Text(), nullable=False),
        sa.Column("subject", sa.String(length=64), nullable=False),
        sa.Column("problem_metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_problems_session_id", "problems", ["session_id"])

    # 6. attempts
    op.create_table(
        "attempts",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("problem_id", sa.String(length=64), sa.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_input", sa.Text(), nullable=False),
        sa.Column("normalized_input", sa.Text(), nullable=True),
        sa.Column("analysis", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_attempts_problem_id", "attempts", ["problem_id"])

    # 7. whiteboard_states
    op.create_table(
        "whiteboard_states",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("explanation_document_id", sa.String(length=64), sa.ForeignKey("explanation_documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("state_json", sa.JSON(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_whiteboard_states_exp_doc_id", "whiteboard_states", ["explanation_document_id"])

    # 8. model_requests
    op.create_table(
        "model_requests",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), sa.ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("request_type", sa.String(length=64), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("token_usage", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_model_requests_session_id", "model_requests", ["session_id"])

    # 9. mistakes
    op.create_table(
        "mistakes",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("concept", sa.String(length=128), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_mistakes_session_id", "mistakes", ["session_id"])

    # 10. idempotency_records
    op.create_table(
        "idempotency_records",
        sa.Column("idempotency_key", sa.String(length=128), primary_key=True, nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("endpoint", sa.String(length=255), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        sa.Column("response_code", sa.Integer(), nullable=False),
        sa.Column("response_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("idempotency_records")
    op.drop_table("mistakes")
    op.drop_table("model_requests")
    op.drop_table("whiteboard_states")
    op.drop_table("attempts")
    op.drop_table("problems")
    op.drop_table("messages")
    op.drop_table("explanation_documents")
    op.drop_table("sessions")
    op.drop_table("users")
