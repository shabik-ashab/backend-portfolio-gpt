"""add task_status to resumes using TaskStatusEnum from model

Revision ID: 427eaecbbf7f
Revises: 9dbd02a8cc89
Create Date: 2025-05-08 21:20:04.361315
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '427eaecbbf7f'
down_revision: Union[str, None] = '9dbd02a8cc89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum values must match your model exactly
task_status_enum = sa.Enum(
    'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED',
    name='taskstatusenum'
)

def upgrade() -> None:
    # Create ENUM type first
    task_status_enum.create(op.get_bind(), checkfirst=True)

    # Check if the column already exists
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'task_status' not in [column['name'] for column in inspector.get_columns('resumes')]:
        op.add_column('resumes', sa.Column(
            'task_status',
            task_status_enum,
            nullable=False,
            server_default='PENDING'
        ))

def downgrade() -> None:
    # Drop the column first
    op.drop_column('resumes', 'task_status')

    # Then drop the ENUM type
    task_status_enum.drop(op.get_bind(), checkfirst=True)
