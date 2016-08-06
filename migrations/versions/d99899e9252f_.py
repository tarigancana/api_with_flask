"""empty message

Revision ID: d99899e9252f
Revises: a605af8daf8b
Create Date: 2016-08-07 04:16:37.636923

"""

# revision identifiers, used by Alembic.
revision = 'd99899e9252f'
down_revision = 'a605af8daf8b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_group', ['group_id'])
    op.create_unique_constraint(None, 'user_group', ['user_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_group', type_='unique')
    op.drop_constraint(None, 'user_group', type_='unique')
    ### end Alembic commands ###
