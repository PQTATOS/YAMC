"""delete setup

Revision ID: 67846672397d
Revises: b6383c539ede
Create Date: 2024-05-25 01:52:34.744289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67846672397d'
down_revision: Union[str, None] = 'b6383c539ede'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_servers_user_id'), 'servers', ['user_id'], unique=False)
    op.drop_constraint('servers_user_id_fkey', 'servers', type_='foreignkey')
    op.create_foreign_key(None, 'servers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'servers', type_='foreignkey')
    op.create_foreign_key('servers_user_id_fkey', 'servers', 'users', ['user_id'], ['id'])
    op.drop_index(op.f('ix_servers_user_id'), table_name='servers')
    # ### end Alembic commands ###
