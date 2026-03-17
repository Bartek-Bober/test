"""create_conversations_table

Revision ID: 339cf1659f44
Revises: 84701be0f93b
Create Date: 2026-03-17 10:54:15.023798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '339cf1659f44'
down_revision: Union[str, None] = '84701be0f93b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id VARCHAR(50) NOT NULL,
        role VARCHAR(20) NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)


def downgrade() -> None:
    pass
