"""auto-add Column Phonenumber

Revision ID: 612621e2c72e
Revises: 9a287f9f75d1
Create Date: 2021-12-04 12:11:37.103995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '612621e2c72e'
down_revision = '9a287f9f75d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
