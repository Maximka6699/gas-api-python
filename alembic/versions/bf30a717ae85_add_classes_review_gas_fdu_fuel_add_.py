"""add classes review, gas, fdu, fuel + add relationships

Revision ID: bf30a717ae85
Revises: d6701a0e2ffb
Create Date: 2024-10-12 00:39:34.527754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf30a717ae85'
down_revision: Union[str, None] = 'd6701a0e2ffb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('FDUs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('service_date', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_FDUs_id'), 'FDUs', ['id'], unique=False)
    op.create_table('Fuels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Fuels_id'), 'Fuels', ['id'], unique=False)
    op.create_table('Gases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('adress', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Gases_id'), 'Gases', ['id'], unique=False)
    op.create_table('Reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('gas_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('review_date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['gas_id'], ['Gases.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Reviews_gas_id'), 'Reviews', ['gas_id'], unique=False)
    op.create_index(op.f('ix_Reviews_id'), 'Reviews', ['id'], unique=False)
    op.create_index(op.f('ix_Reviews_user_id'), 'Reviews', ['user_id'], unique=False)
    op.alter_column('Users', 'regdate',
               existing_type=sa.DATE(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.create_index(op.f('ix_Users_id'), 'Users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Users_id'), table_name='Users')
    op.alter_column('Users', 'regdate',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATE(),
               existing_nullable=True)
    op.drop_index(op.f('ix_Reviews_user_id'), table_name='Reviews')
    op.drop_index(op.f('ix_Reviews_id'), table_name='Reviews')
    op.drop_index(op.f('ix_Reviews_gas_id'), table_name='Reviews')
    op.drop_table('Reviews')
    op.drop_index(op.f('ix_Gases_id'), table_name='Gases')
    op.drop_table('Gases')
    op.drop_index(op.f('ix_Fuels_id'), table_name='Fuels')
    op.drop_table('Fuels')
    op.drop_index(op.f('ix_FDUs_id'), table_name='FDUs')
    op.drop_table('FDUs')
    # ### end Alembic commands ###
