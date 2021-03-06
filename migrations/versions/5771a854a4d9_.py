"""empty message

Revision ID: 5771a854a4d9
Revises: 2f23e4c0cbb9
Create Date: 2016-08-07 01:11:00.578471

"""

# revision identifiers, used by Alembic.
revision = '5771a854a4d9'
down_revision = '2f23e4c0cbb9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group')
    op.drop_table('groups')
    ### end Alembic commands ###
