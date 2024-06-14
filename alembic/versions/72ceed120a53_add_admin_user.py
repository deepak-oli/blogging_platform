"""Add admin user

Revision ID: 72ceed120a53
Revises: 22ccf3ceaa5a
Create Date: 2024-06-14 08:45:42.161436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column



# revision identifiers, used by Alembic.
revision: str = '72ceed120a53'
down_revision: Union[str, None] = '22ccf3ceaa5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = table('user',
        column('username', sa.String),
        column('password', sa.String),
        column('role', sa.String)
    )


def downgrade() -> None:
    pass
