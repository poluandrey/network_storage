"""devica_network_unique_constraint

Revision ID: c0fd378da1e9
Revises: 41bad83a77b2
Create Date: 2024-03-19 15:26:32.939072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0fd378da1e9'
down_revision: Union[str, None] = '41bad83a77b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('device_network_unique_constraint', 'network_interface', ['device_id', 'ip_addresses'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('device_network_unique_constraint', 'network_interface', type_='unique')
    # ### end Alembic commands ###
