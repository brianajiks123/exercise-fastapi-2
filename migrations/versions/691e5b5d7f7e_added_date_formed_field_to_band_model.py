"""Added date formed field to Band model

Revision ID: 691e5b5d7f7e
Revises: 4f24704b2a67
Create Date: 2024-11-28 22:48:37.457757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '691e5b5d7f7e'
down_revision: Union[str, None] = '4f24704b2a67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('band', sa.Column('date_formed', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('band', 'date_formed')
    # ### end Alembic commands ###
