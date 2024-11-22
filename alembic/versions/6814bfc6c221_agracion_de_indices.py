"""agracion_de_indices

Revision ID: 6814bfc6c221
Revises: 704fadc734cd
Create Date: 2024-11-22 10:23:46.680000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6814bfc6c221'
down_revision: Union[str, None] = '704fadc734cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_caserios_centro_poblado_id'), 'caserios', ['centro_poblado_id'], unique=False)
    op.create_index(op.f('ix_comunicacion_areas_area_origen_id'), 'comunicacion_areas', ['area_origen_id'], unique=False)
    op.create_index(op.f('ix_remitentes_apellido_paterno'), 'remitentes', ['apellido_paterno'], unique=False)
    op.create_index(op.f('ix_remitentes_nombres'), 'remitentes', ['nombres'], unique=False)
    op.create_index(op.f('ix_trabajadores_apellido_paterno'), 'trabajadores', ['apellido_paterno'], unique=False)
    op.create_index(op.f('ix_trabajadores_area_id'), 'trabajadores', ['area_id'], unique=False)
    op.create_index(op.f('ix_trabajadores_nombres'), 'trabajadores', ['nombres'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trabajadores_nombres'), table_name='trabajadores')
    op.drop_index(op.f('ix_trabajadores_area_id'), table_name='trabajadores')
    op.drop_index(op.f('ix_trabajadores_apellido_paterno'), table_name='trabajadores')
    op.drop_index(op.f('ix_remitentes_nombres'), table_name='remitentes')
    op.drop_index(op.f('ix_remitentes_apellido_paterno'), table_name='remitentes')
    op.drop_index(op.f('ix_comunicacion_areas_area_origen_id'), table_name='comunicacion_areas')
    op.drop_index(op.f('ix_caserios_centro_poblado_id'), table_name='caserios')
    # ### end Alembic commands ###