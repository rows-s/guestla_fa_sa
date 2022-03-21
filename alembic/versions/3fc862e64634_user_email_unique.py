"""user.email unique

Revision ID: 3fc862e64634
Revises: 771f57a6336b
Create Date: 2022-03-21 14:44:30.625208

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '3fc862e64634'
down_revision = '771f57a6336b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uq_user_email', 'users', ['email'])


def downgrade():
    op.drop_constraint('uq_user_name', 'user')
