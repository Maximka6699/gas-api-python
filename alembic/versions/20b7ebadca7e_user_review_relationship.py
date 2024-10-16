"""user review relationship

Revision ID: 20b7ebadca7e
Revises: 8c51479061eb
Create Date: 2024-10-16 14:08:43.191430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20b7ebadca7e'
down_revision: Union[str, None] = '8c51479061eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('review_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_Users_review_id'), 'Users', ['review_id'], unique=False)
    op.create_foreign_key(None, 'Users', 'Reviews', ['review_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Users', type_='foreignkey')
    op.drop_index(op.f('ix_Users_review_id'), table_name='Users')
    op.drop_column('Users', 'review_id')
    # ### end Alembic commands ###
