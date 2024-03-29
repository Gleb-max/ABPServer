"""empty message

Revision ID: fa6586e3e9d7
Revises: e3274a26968b
Create Date: 2021-03-19 06:05:26.979225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa6586e3e9d7'
down_revision = 'e3274a26968b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subject', schema=None) as batch_op:
        # batch_op.drop_constraint('subject', type_='foreignkey')
        batch_op.drop_column('teacher_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teacher_id', sa.INTEGER(), nullable=True))
        # batch_op.create_foreign_key('subject', 'teacher', ['teacher_id'], ['id'])

    # ### end Alembic commands ###
