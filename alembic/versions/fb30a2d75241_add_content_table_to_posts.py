"""add content table to posts

Revision ID: fb30a2d75241
Revises: c56fcabb6f12
Create Date: 2026-07-02 15:50:26.974439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb30a2d75241'
down_revision: Union[str, Sequence[str], None] = 'c56fcabb6f12'
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
