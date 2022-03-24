"""create users table

Revision ID: 49cd567e1f9f
Revises: 
Create Date: 2022-03-24 14:01:36.788963

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '49cd567e1f9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('users')
