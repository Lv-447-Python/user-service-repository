"""empty message

Revision ID: 2348ebd4dcc4
Revises: 18d9b4530232
Create Date: 2019-11-03 13:35:47.747823

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2348ebd4dcc4'
down_revision = '18d9b4530232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('user_email', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('user_password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('user_first_name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('user_last_name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('user_image_file', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('user_registration_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('user_email', name='users_user_email_key'),
    sa.UniqueConstraint('user_name', name='users_user_name_key')
    )
    # ### end Alembic commands ###
