"""add user table

Revision ID: 307692eb3da4
Revises: 5bbc9af349e8
Create Date: 2021-12-02 17:42:11.201429

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, TIMESTAMP


# revision identifiers, used by Alembic.
revision = '307692eb3da4'
down_revision = '5bbc9af349e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),  
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
