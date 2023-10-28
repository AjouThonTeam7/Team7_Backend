"""empty message

Revision ID: 6c760092ce8b
Revises: 1eacc7e2c4c7
Create Date: 2023-10-29 02:50:38.784255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c760092ce8b'
down_revision = '1eacc7e2c4c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_name')
    # ### end Alembic commands ###
