"""create posts table

Revision ID: 164823b6cf1f
Revises: 
Create Date: 2024-02-26 00:01:52.870305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '164823b6cf1f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), primary_key=True, nullable=False), sa.Column("title",sa.String, nullable=False))
    


def downgrade() -> None:
    op.drop_table("posts")
    
