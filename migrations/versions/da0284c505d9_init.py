"""init

Revision ID: da0284c505d9
Revises: 
Create Date: 2023-04-23 22:29:33.515240

"""
import sqlalchemy as sa
from alembic import op


revision = 'da0284c505d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'city',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('lat', sa.DECIMAL(), nullable=False),
        sa.Column('lon', sa.DECIMAL(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('city')
