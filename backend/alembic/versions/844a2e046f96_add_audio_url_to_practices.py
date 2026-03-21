"""add audio_url to practices

Revision ID: 844a2e046f96
Revises: 79fc43444ec6
Create Date: 2026-03-22 10:28:25.110042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '844a2e046f96'
down_revision: Union[str, None] = '79fc43444ec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
