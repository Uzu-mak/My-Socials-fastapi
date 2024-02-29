"""add foreign key to post table

Revision ID: 0bc1c5ed3865
Revises: b72e0f1db98b
Create Date: 2024-02-26 01:03:21.011554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bc1c5ed3865'
down_revision: Union[str, None] = 'b72e0f1db98b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
        sa.Column("owner_id", sa.Integer() , nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts",referent_table= "users", local_cols=["owner_id"], remote_cols=["id"],ondelete="CASCADE")
       
                  
    


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name = "posts")
    op.drop_column("posts","owner_id")
    pass
