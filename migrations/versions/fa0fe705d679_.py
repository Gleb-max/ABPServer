"""empty message

Revision ID: fa0fe705d679
Revises: ab61a316eb87
Create Date: 2021-03-19 00:36:26.636276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa0fe705d679'
down_revision = 'ab61a316eb87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enrollee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('achievements_scan', sa.String(length=300), nullable=True))

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('group_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_number', sa.VARCHAR(length=20), nullable=True))

    with op.batch_alter_table('enrollee', schema=None) as batch_op:
        batch_op.drop_column('achievements_scan')

    # ### end Alembic commands ###
