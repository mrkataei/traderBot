"""watchlist strategy added

Revision ID: fda42c12abb9
Revises: 
Create Date: 2023-01-21 22:47:55.839898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fda42c12abb9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('cost', sa.String(length=15), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('watchlist_number', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plan_cost'), 'plan', ['cost'], unique=False)
    op.create_index(op.f('ix_plan_description'), 'plan', ['description'], unique=False)
    op.create_index(op.f('ix_plan_duration'), 'plan', ['duration'], unique=False)
    op.create_index(op.f('ix_plan_id'), 'plan', ['id'], unique=False)
    op.create_index(op.f('ix_plan_name'), 'plan', ['name'], unique=True)
    op.create_index(op.f('ix_plan_watchlist_number'), 'plan', ['watchlist_number'], unique=False)
    op.create_table('strategy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_strategy_description'), 'strategy', ['description'], unique=False)
    op.create_index(op.f('ix_strategy_id'), 'strategy', ['id'], unique=False)
    op.create_index(op.f('ix_strategy_name'), 'strategy', ['name'], unique=False)
    op.create_table('user',
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('chat_id', sa.String(length=15), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('signup_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('valid_time_plan', sa.DateTime(timezone=True), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_index(op.f('ix_user_chat_id'), 'user', ['chat_id'], unique=True)
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('watchlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=True),
    sa.Column('asset', sa.String(length=15), nullable=True),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('exchange', sa.String(length=15), nullable=True),
    sa.Column('public_key', sa.String(length=60), nullable=False),
    sa.Column('secrete_key', sa.String(length=60), nullable=False),
    sa.Column('strategy_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['strategy_id'], ['strategy.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_watchlist_asset'), 'watchlist', ['asset'], unique=False)
    op.create_index(op.f('ix_watchlist_exchange'), 'watchlist', ['exchange'], unique=False)
    op.create_index(op.f('ix_watchlist_id'), 'watchlist', ['id'], unique=False)
    op.create_index(op.f('ix_watchlist_name'), 'watchlist', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_watchlist_name'), table_name='watchlist')
    op.drop_index(op.f('ix_watchlist_id'), table_name='watchlist')
    op.drop_index(op.f('ix_watchlist_exchange'), table_name='watchlist')
    op.drop_index(op.f('ix_watchlist_asset'), table_name='watchlist')
    op.drop_table('watchlist')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_index(op.f('ix_user_chat_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_strategy_name'), table_name='strategy')
    op.drop_index(op.f('ix_strategy_id'), table_name='strategy')
    op.drop_index(op.f('ix_strategy_description'), table_name='strategy')
    op.drop_table('strategy')
    op.drop_index(op.f('ix_plan_watchlist_number'), table_name='plan')
    op.drop_index(op.f('ix_plan_name'), table_name='plan')
    op.drop_index(op.f('ix_plan_id'), table_name='plan')
    op.drop_index(op.f('ix_plan_duration'), table_name='plan')
    op.drop_index(op.f('ix_plan_description'), table_name='plan')
    op.drop_index(op.f('ix_plan_cost'), table_name='plan')
    op.drop_table('plan')
    # ### end Alembic commands ###
