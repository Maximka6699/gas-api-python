"""gas

Revision ID: 42205b79d329
Revises: e74d13d1e88f
Create Date: 2024-10-21 23:52:58.712485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42205b79d329'
down_revision: Union[str, None] = 'e74d13d1e88f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Gases', 'photo',
               existing_type=sa.VARCHAR(),
               type_=sa.JSON(),
               postgresql_using='photo::json',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Gases', 'photo',
               existing_type=sa.JSON(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
