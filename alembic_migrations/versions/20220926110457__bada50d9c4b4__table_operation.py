"""Table operation

Revision ID: bada50d9c4b4
Revises: 
Create Date: 2022-09-26 11:04:57.133386

"""
from alembic import op
import sqlalchemy as sa

from my_awesome_app.infrastructure.orm.custom_types import DecimalType

# revision identifiers, used by Alembic.
revision = 'bada50d9c4b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'operation',
        sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
        sa.Column('a', DecimalType(precision=64, scale=32), nullable=False),
        sa.Column('operation', sa.String(length=10), nullable=False),
        sa.Column('b', DecimalType(precision=64, scale=32), nullable=False),
        sa.Column('result', DecimalType(precision=64, scale=32), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('operation')
