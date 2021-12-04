"""add foreign-key to posts table

Revision ID: 5437e5c012b6
Revises: 307692eb3da4
Create Date: 2021-12-04 11:30:37.553056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5437e5c012b6'
down_revision = '307692eb3da4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
