"""add foreign key constraint

Revision ID: 4972eebf3a8d
Revises: 29c52ab7fb74
Create Date: 2022-11-23 13:08:17.381732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4972eebf3a8d'
down_revision = '29c52ab7fb74'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('mangas', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('manga_users_fk', source_table="mangas", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="mangas")
    op.drop_column('mangas', 'owner_id')
    pass
