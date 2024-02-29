"""add content column to post table

Revision ID: 69e894717a95
Revises: 164823b6cf1f
Create Date: 2024-02-26 00:31:19.567940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69e894717a95'
down_revision: Union[str, None] = '164823b6cf1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(),nullable=False))
    


def downgrade() -> None:
    op.drop_column("posts", "content")
    
