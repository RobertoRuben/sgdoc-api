import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.dialects.postgresql import ENUM
from urllib.parse import quote_plus

from alembic import context

# Agregar el directorio 'src' al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.config.settings import settings  # Configuración de tu aplicación
from src.db.database import SQLModel  # Definición de tus modelos con SQLModel
from src.model.entity import *  # Importar tus modelos definidos

# Configuración de logging
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

# Metadata de los modelos
target_metadata = SQLModel.metadata

print("Tablas detectadas por Alembic:", SQLModel.metadata.tables.keys())

def get_database_url():
    password = quote_plus(settings.POSTGRES_PASSWORD)
    return (
        f"postgresql://{settings.POSTGRES_USER}:{password}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    ).replace('%', '%%')

config = context.config
config.set_main_option('sqlalchemy.url', get_database_url())

# Personalización para manejar tipos ENUM
def render_item(type_, obj, autogen_context):
    """Renderiza los tipos ENUM correctamente con create_type=False."""
    if isinstance(obj, ENUM):
        autogen_context.imports.add("from sqlalchemy.dialects.postgresql import ENUM")
        enum_values = ", ".join([f"'{e}'" for e in obj.enums])
        return f"ENUM({enum_values}, name='{obj.name}', create_type=False)"
    return False

def include_object(object, name, type_, reflected, compare_to):
    """Incluir todos los objetos excepto ENUMs reflejados que no queremos recrear."""
    if isinstance(object, ENUM) and reflected:
        return False  # Ignorar ENUMs reflejados
    return True

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            include_object=include_object,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
