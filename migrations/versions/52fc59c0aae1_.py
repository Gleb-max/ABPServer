"""empty message

Revision ID: 52fc59c0aae1
Revises: 9c6b90c2364f
Create Date: 2021-03-17 00:29:52.739475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52fc59c0aae1'
down_revision = '9c6b90c2364f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('study_direction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('budget_count', sa.SmallInteger(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('study_direction', schema=None) as batch_op:
        batch_op.drop_column('budget_count')

    # ### end Alembic commands ###
