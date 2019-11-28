"""empty message

Revision ID: d8701561868d
Revises: 
Create Date: 2019-11-28 22:32:23.065054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8701561868d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(length=25), nullable=False),
    sa.Column('user_email', sa.String(length=35), nullable=False),
    sa.Column('user_password', sa.String(length=255), nullable=False),
    sa.Column('user_first_name', sa.String(length=25), nullable=False),
    sa.Column('user_last_name', sa.String(length=25), nullable=False),
    sa.Column('user_image_file', sa.String(length=25), nullable=False),
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
