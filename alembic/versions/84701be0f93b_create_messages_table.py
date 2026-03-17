"""create_messages_table

Revision ID: 84701be0f93b
Revises: 
Create Date: 2026-03-17 10:50:45.057624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84701be0f93b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    );
    """)


def downgrade() -> None:
    pass
