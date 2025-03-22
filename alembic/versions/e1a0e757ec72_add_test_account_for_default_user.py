"""Add test account for default user

Revision ID: e1a0e757ec72
Revises: 493247aff8b8
Create Date: 2025-03-22 10:46:44.710295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1a0e757ec72'
down_revision: Union[str, None] = '493247aff8b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавление тестового счёта для тестового пользователя
    op.execute("""
        INSERT INTO accounts (user_id, balance)
        SELECT id, 1000.0
        FROM users
        WHERE email = 'user@example.com';
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаление тестового счёта при откате миграции
    op.execute("""
        DELETE FROM accounts
        WHERE user_id = (
            SELECT id
            FROM users
            WHERE email = 'user@example.com'
        );
    """)
