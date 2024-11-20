from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import create_db_and_tables
from src.controller.remitente_controller import router as remitente_router, remitentes_tag_metadata
from src.controller.categoria_controller import router as categoria_router, categorias_tag_metadata
from src.controller.ambito_controller import router as ambito_router, ambitos_tag_metadata
from src.controller.centro_poblado_controller import router as centro_poblado_router, centros_poblados_tag_metadata
from src.controller.caserio_controller import router as caserio_router, caserios_tag_metadata
from src.controller.rol_controller import router as rol_router, roles_tag_metadata
from src.controller.area_controller import router as area_router, areas_tag_metadata
from src.controller.comunicacion_area_controller import router as comunicacion_area_router, comunicaciones_area_tag_metadata

tags_metadata = [
    remitentes_tag_metadata,
    categorias_tag_metadata,
    ambitos_tag_metadata,
    centros_poblados_tag_metadata,
    caserios_tag_metadata,
    roles_tag_metadata,
    areas_tag_metadata,
    comunicaciones_area_tag_metadata
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
app.include_router(ambito_router, prefix="/api/v1")
app.include_router(centro_poblado_router, prefix="/api/v1")
app.include_router(caserio_router, prefix="/api/v1")
app.include_router(rol_router, prefix="/api/v1")
app.include_router(area_router, prefix="/api/v1")
app.include_router(comunicacion_area_router, prefix="/api/v1")