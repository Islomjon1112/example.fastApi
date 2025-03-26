"""add content column to posts table

Revision ID: ec6dad3b9126
Revises: 8a5e0f26016b
Create Date: 2025-03-24 22:52:35.461992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec6dad3b9126'
down_revision: Union[str, None] = '8a5e0f26016b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
