"""add last few columns to post table

Revision ID: 72af3f4f0ed0
Revises: 0bc1c5ed3865
Create Date: 2024-02-26 01:20:41.896073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72af3f4f0ed0'
down_revision: Union[str, None] = '0bc1c5ed3865'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(),nullable=False,server_default="TRUE"))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text("NOW()")))
    


def downgrade():
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
            
    
