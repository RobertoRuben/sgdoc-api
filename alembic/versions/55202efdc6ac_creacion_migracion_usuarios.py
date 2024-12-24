"""creacion_migracion_usuarios

Revision ID: 55202efdc6ac
Revises: 6814bfc6c221
Create Date: 2024-12-01 23:41:04.784075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55202efdc6ac'
down_revision: Union[str, None] = '6814bfc6c221'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Creación de la tabla 'usuarios'
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre_usuario', sa.Text(), nullable=True),
        sa.Column('contrasena', sa.Text(), nullable=True),
        sa.Column('fecha_creacion', sa.TIMESTAMP(), nullable=True),
        sa.Column('fecha_actualizacion', sa.TIMESTAMP(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('rol_id', sa.Integer(), nullable=False),
        sa.Column('trabajador_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['rol_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['trabajador_id'], ['trabajadores.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('trabajador_id')
    )

    # Obtiene la conexión y el inspector para verificar índices existentes
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    def create_index_if_not_exists(table_name: str, index_name: str, columns: list[str], unique: bool = False):
        existing_indexes = {idx['name'] for idx in inspector.get_indexes(table_name)}
        if index_name not in existing_indexes:
            op.create_index(index_name, table_name, columns, unique=unique)
        else:
            print(f"El índice {index_name} ya existe en {table_name}, se omite su creación.")

    # Crear índices solo si no existen previamente
    create_index_if_not_exists('usuarios', op.f('ix_usuarios_nombre_usuario'), ['nombre_usuario'], unique=True)
    create_index_if_not_exists('caserios', op.f('ix_caserios_centro_poblado_id'), ['centro_poblado_id'], unique=False)
    create_index_if_not_exists('comunicacion_areas', op.f('ix_comunicacion_areas_area_origen_id'), ['area_origen_id'], unique=False)
    create_index_if_not_exists('remitentes', op.f('ix_remitentes_apellido_paterno'), ['apellido_paterno'], unique=False)
    create_index_if_not_exists('remitentes', op.f('ix_remitentes_nombres'), ['nombres'], unique=False)
    create_index_if_not_exists('trabajadores', op.f('ix_trabajadores_apellido_paterno'), ['apellido_paterno'], unique=False)
    create_index_if_not_exists('trabajadores', op.f('ix_trabajadores_area_id'), ['area_id'], unique=False)
    create_index_if_not_exists('trabajadores', op.f('ix_trabajadores_nombres'), ['nombres'], unique=False)


def downgrade() -> None:
    # Eliminar índices y tabla 'usuarios'
    op.drop_index(op.f('ix_trabajadores_nombres'), table_name='trabajadores')
    op.drop_index(op.f('ix_trabajadores_area_id'), table_name='trabajadores')
    op.drop_index(op.f('ix_trabajadores_apellido_paterno'), table_name='trabajadores')
    op.drop_index(op.f('ix_remitentes_nombres'), table_name='remitentes')
    op.drop_index(op.f('ix_remitentes_apellido_paterno'), table_name='remitentes')
    op.drop_index(op.f('ix_comunicacion_areas_area_origen_id'), table_name='comunicacion_areas')
    op.drop_index(op.f('ix_caserios_centro_poblado_id'), table_name='caserios')
    op.drop_index(op.f('ix_usuarios_nombre_usuario'), table_name='usuarios')
    op.drop_table('usuarios')
