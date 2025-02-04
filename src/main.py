from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.exception.handlers import register_exception_handlers
from src.db.database import create_db_and_tables
from src.controller.auth_controller import get_current_user
from src.controller.auth_controller import router as auth_router
from src.controller.remitente_controller import router as remitente_router, remitentes_tag_metadata
from src.controller.categoria_controller import router as categoria_router, categorias_tag_metadata
from src.controller.ambito_controller import router as ambito_router, ambitos_tag_metadata
from src.controller.centro_poblado_controller import router as centro_poblado_router, centros_poblados_tag_metadata
from src.controller.caserio_controller import router as caserio_router, caserios_tag_metadata
from src.controller.rol_controller import router as rol_router, roles_tag_metadata
from src.controller.area_controller import router as area_router, areas_tag_metadata
from src.controller.comunicacion_area_controller import router as comunicacion_area_router, comunicaciones_area_tag_metadata
from src.controller.trabajador_controller import router as trabajador_router, trabajadores_tag_metadata
from src.controller.usuario_controller import router as usuario_router, usuarios_metadata
from src.controller.documento_controller import router as documento_router, documentos_tag_metadata
from src.controller.derivacion_controller import router as derivacion_router, derivaciones_tag_metadata
from src.controller.detalle_derivacion_controller import router as detalle_derivacion_router, detalle_derivaciones_tag_metadata
from src.controller.estado_documento_controller import router as estado_documento_router, estado_documento_tag_metadata
from src.controller.dashboard_mesa_partes_controller import router as documents_by_current_date_router, documentos_by_current_date_tag_metadata
import logging
logging.basicConfig(level=logging.INFO)

allowed_subnets = [
    "127.0.0.1",
    "192.168.1.",
    "192.168.2.",
    "172.23.32.",
    "localhost",
    "172.25.208.",
    "172.27.32."
]

tags_metadata = [
    remitentes_tag_metadata,
    categorias_tag_metadata,
    ambitos_tag_metadata,
    centros_poblados_tag_metadata,
    caserios_tag_metadata,
    roles_tag_metadata,
    areas_tag_metadata,
    comunicaciones_area_tag_metadata,
    trabajadores_tag_metadata,
    usuarios_metadata,
    documentos_tag_metadata,
    derivaciones_tag_metadata,
    detalle_derivaciones_tag_metadata,
    estado_documento_tag_metadata,
    documentos_by_current_date_tag_metadata
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="SGDOC API",
    description="API para el Sistema de Gestión de Documentos",
    version="0.1.0",
    openapi_tags=tags_metadata,
    debug=True,
    lifespan=lifespan
)

register_exception_handlers(app)

@app.middleware("http")
async def ip_restriction_middleware(request: Request, call_next):
    client_ip = request.client.host
    logging.info(f"Client IP: {client_ip}")  # Registro de la IP del cliente
    if not any(client_ip.startswith(subnet) for subnet in allowed_subnets):
        logging.warning(f"Access denied for IP: {client_ip}")
        raise HTTPException(status_code=403, detail="Access forbidden: your IP address is not allowed")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto más si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(remitente_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(categoria_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(ambito_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(centro_poblado_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(caserio_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(rol_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(area_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(comunicacion_area_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(trabajador_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(usuario_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(documento_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(derivacion_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(detalle_derivacion_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(estado_documento_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])
app.include_router(documents_by_current_date_router, prefix="/api/v1", dependencies=[Depends(get_current_user)])