"""add content column to posts table

Revision ID: 5bbc9af349e8
Revises: 6729b08a8964
Create Date: 2021-12-02 17:28:38.060807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bbc9af349e8'
down_revision = '6729b08a8964'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
