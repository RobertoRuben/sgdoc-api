from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import create_db_and_tables
from src.controller.remitente_controller import router as remitente_router, remitentes_tag_metadata
from src.controller.categoria_controller import router as categoria_router, categorias_tag_metadata

tags_metadata = [
    remitentes_tag_metadata,
    categorias_tag_metadata
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="SGDOC API",
    description="API para el Sistema de Gestión de Documentos",
    version="1.0.0",
    openapi_tags=tags_metadata,
    debug=True,
    lifespan=lifespan
)

app.include_router(remitente_router, prefix="/api/v1")
app.include_router(categoria_router, prefix="/api/v1")