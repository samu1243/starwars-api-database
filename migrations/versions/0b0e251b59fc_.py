"""empty message

Revision ID: 0b0e251b59fc
Revises: 2f2a1a578fd3
Create Date: 2022-06-06 22:07:55.870560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b0e251b59fc'
down_revision = '2f2a1a578fd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('_id', sa.String(length=150), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('people', '_id')
    # ### end Alembic commands ###
