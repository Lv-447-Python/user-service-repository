"""empty message

Revision ID: f3138534d62b
Revises: 2348ebd4dcc4
Create Date: 2019-11-03 13:40:53.133315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3138534d62b'
down_revision = '2348ebd4dcc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=15), nullable=False),
    sa.Column('user_email', sa.String(length=15), nullable=False),
    sa.Column('user_password', sa.String(length=255), nullable=False),
    sa.Column('user_first_name', sa.String(length=15), nullable=False),
    sa.Column('user_last_name', sa.String(length=15), nullable=False),
    sa.Column('user_image_file', sa.String(length=15), nullable=False),
    sa.Column('user_registration_data', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email'),
    sa.UniqueConstraint('user_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###