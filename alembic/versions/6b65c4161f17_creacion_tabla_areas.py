"""creacion_tabla_areas

Revision ID: 6b65c4161f17
Revises: 0d14befc0ec0
Create Date: 2024-11-16 17:45:13.162942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b65c4161f17'
down_revision: Union[str, None] = '0d14befc0ec0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('areas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_area', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre_area')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('areas')
    # ### end Alembic commands ###