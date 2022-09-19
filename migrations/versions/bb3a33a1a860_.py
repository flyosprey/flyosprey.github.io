"""empty message

Revision ID: bb3a33a1a860
Revises: 
Create Date: 2022-09-14 15:47:24.060908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb3a33a1a860'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks_to_do',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('task_title', sa.String(), nullable=False),
    sa.Column('task_description', sa.String(length=200), nullable=True),
    sa.Column('responsible_of_task', sa.String(length=120), nullable=True),
    sa.Column('creation_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('task_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_to_do')
    # ### end Alembic commands ###