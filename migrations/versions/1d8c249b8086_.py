"""empty message

Revision ID: 1d8c249b8086
Revises: 25696e0dbd62
Create Date: 2014-01-26 04:03:45.648492

"""

# revision identifiers, used by Alembic.
revision = '1d8c249b8086'
down_revision = '25696e0dbd62'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('alliance_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('alliance_name', sa.String(length=51), nullable=True))
    op.add_column('user', sa.Column('character_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('character_name', sa.String(length=25), nullable=True))
    op.add_column('user', sa.Column('corporation_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('corporation_name', sa.String(length=51), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'username')
    op.drop_column('user', 'corporation_name')
    op.drop_column('user', 'corporation_id')
    op.drop_column('user', 'character_name')
    op.drop_column('user', 'character_id')
    op.drop_column('user', 'alliance_name')
    op.drop_column('user', 'alliance_id')
    ### end Alembic commands ###