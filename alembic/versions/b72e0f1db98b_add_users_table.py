"""add users table

Revision ID: b72e0f1db98b
Revises: 69e894717a95
Create Date: 2024-02-26 00:43:42.440318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b72e0f1db98b'
down_revision: Union[str, None] = '69e894717a95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.Integer(),nullable=False),
        sa.Column("email", sa.String(),nullable=False),
        sa.Column("password", sa.String(),nullable=False),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
        )
    


def downgrade() -> None:
    op.drop_table("users")
