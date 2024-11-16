# alembic/env.py

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Agregar el directorio src al sys.path para importar módulos correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Importar las configuraciones y modelos
from src.config.settings import settings
from src.db.database import engine, SQLModel
from src.model.entity import *

# Configuración de Alembic
config = context.config

# Configurar el logging según el archivo de configuración
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establecer target_metadata a la metadata de SQLModel
target_metadata = SQLModel.metadata
# Después de establecer target_metadata
print("Tablas detectadas por Alembic:", SQLModel.metadata.tables.keys())

# Configurar la URL de la base de datos desde las configuraciones de tu aplicación
def get_database_url():
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

config.set_main_option('sqlalchemy.url', get_database_url())

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
