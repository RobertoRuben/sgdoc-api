"""creacion_tabla_trabajadores

Revision ID: 704fadc734cd
Revises: 2fd210dde28a
Create Date: 2024-11-20 12:09:27.041906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = '704fadc734cd'
down_revision: Union[str, None] = '2fd210dde28a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear el tipo ENUM solo si no existe
    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'generoenum') THEN
            CREATE TYPE generoenum AS ENUM ('masculino', 'femenino');
        END IF;
    END $$;
    """)

    # Crear la tabla 'trabajadores'
    op.create_table(
        'trabajadores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dni', sa.Integer(), nullable=False),
        sa.Column('nombres', sa.Text(), nullable=True),
        sa.Column('apellido_paterno', sa.Text(), nullable=True),
        sa.Column('apellido_materno', sa.Text(), nullable=True),
        sa.Column('genero', ENUM('masculino', 'femenino', name='generoenum', create_type=False), nullable=False),  # Usar el tipo existente
        sa.Column('area_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['area_id'], ['areas.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dni')
    )


def downgrade() -> None:
    # Eliminar la tabla 'trabajadores'
    op.drop_table('trabajadores')

    # Eliminar el tipo ENUM solo si no se utiliza
    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE udt_name = 'generoenum'
        ) THEN
            DROP TYPE generoenum;
        END IF;
    END $$;
    """)
