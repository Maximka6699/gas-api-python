"""исправление2

Revision ID: 6ba57fb3deac
Revises: 28084815c02c
Create Date: 2024-10-12 14:30:00.011433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ba57fb3deac'
down_revision: Union[str, None] = '28084815c02c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Fuels', sa.Column('fdus_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Fuels', 'FDUs', ['fdus_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Fuels', type_='foreignkey')
    op.drop_column('Fuels', 'fdus_id')
    # ### end Alembic commands ###
