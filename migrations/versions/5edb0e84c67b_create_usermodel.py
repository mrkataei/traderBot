"""create usermodel

Revision ID: 5edb0e84c67b
Revises: c953cbbafa32
Create Date: 2023-01-20 12:20:46.101487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5edb0e84c67b'
down_revision = 'c953cbbafa32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('cost', sa.String(length=15), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('sterategy_number', sa.Integer(), nullable=True),
    sa.Column('account_number', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plan_account_number'), 'plan', ['account_number'], unique=False)
    op.create_index(op.f('ix_plan_cost'), 'plan', ['cost'], unique=False)
    op.create_index(op.f('ix_plan_description'), 'plan', ['description'], unique=False)
    op.create_index(op.f('ix_plan_duration'), 'plan', ['duration'], unique=False)
    op.create_index(op.f('ix_plan_id'), 'plan', ['id'], unique=False)
    op.create_index(op.f('ix_plan_name'), 'plan', ['name'], unique=False)
    op.create_index(op.f('ix_plan_sterategy_number'), 'plan', ['sterategy_number'], unique=False)
    op.add_column('user', sa.Column('valid_time_plan', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'valid_time_plan')
    op.drop_index(op.f('ix_plan_sterategy_number'), table_name='plan')
    op.drop_index(op.f('ix_plan_name'), table_name='plan')
    op.drop_index(op.f('ix_plan_id'), table_name='plan')
    op.drop_index(op.f('ix_plan_duration'), table_name='plan')
    op.drop_index(op.f('ix_plan_description'), table_name='plan')
    op.drop_index(op.f('ix_plan_cost'), table_name='plan')
    op.drop_index(op.f('ix_plan_account_number'), table_name='plan')
    op.drop_table('plan')
    # ### end Alembic commands ###
