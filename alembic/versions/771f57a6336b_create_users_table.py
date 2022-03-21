"""create users table

Revision ID: 771f57a6336b
Revises: 
Create Date: 2022-03-21 10:07:16.101180

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '771f57a6336b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String),
        sa.Column('password', sa.String),
    )


def downgrade():
    op.drop_table('users')
