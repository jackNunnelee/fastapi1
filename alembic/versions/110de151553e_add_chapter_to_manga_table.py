"""add chapter to manga table

Revision ID: 110de151553e
Revises: 91856bea66d6
Create Date: 2022-11-23 12:57:43.148088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '110de151553e'
down_revision = '91856bea66d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('mangas', sa.Column('chapter', sa.Integer(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('mangas', 'content')
    pass
