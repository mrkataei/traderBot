"""watchlist strategy added

Revision ID: a979f57eff8c
Revises: 8f31f7038c73
Create Date: 2023-01-26 14:56:21.954759

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a979f57eff8c'
down_revision = '8f31f7038c73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommendation', sa.Column('strategy', sa.String(length=15), nullable=True))
    op.drop_index('ix_recommendation_startegy', table_name='recommendation')
    op.create_index(op.f('ix_recommendation_strategy'), 'recommendation', ['strategy'], unique=False)
    op.drop_column('recommendation', 'startegy')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommendation', sa.Column('startegy', mysql.VARCHAR(length=15), nullable=True))
    op.drop_index(op.f('ix_recommendation_strategy'), table_name='recommendation')
    op.create_index('ix_recommendation_startegy', 'recommendation', ['startegy'], unique=False)
    op.drop_column('recommendation', 'strategy')
    # ### end Alembic commands ###