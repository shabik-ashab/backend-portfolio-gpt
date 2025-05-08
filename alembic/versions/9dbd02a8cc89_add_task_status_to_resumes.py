"""add task_status to resumes

Revision ID: 9dbd02a8cc89
Revises: eb117c28ee78
Create Date: 2025-05-08 21:10:43.362217
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9dbd02a8cc89'
down_revision: Union[str, None] = 'eb117c28ee78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the ENUM type
task_status_enum = postgresql.ENUM(
    'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED',
    name='taskstatusenum'
)

def upgrade() -> None:
    """Upgrade schema."""
    # Explicitly create enum type before using
    task_status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('resumes', sa.Column(
        'task_status',
        task_status_enum,
        server_default='PENDING',
        nullable=False
    ))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('resumes', 'task_status')
    task_status_enum.drop(op.get_bind(), checkfirst=True)
