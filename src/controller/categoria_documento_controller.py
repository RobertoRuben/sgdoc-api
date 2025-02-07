from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto import CategoriaDocumentoRequestDTO, CategoriaDocumentoResponseDTO, PaginatedResponseDTO
from src.service import CategoriaDocumentoService
from src.service.imp import CategoriaDocumentoServiceImp

def get_categoria_documento_service_imp(service: CategoriaDocumentoServiceImp = Depends()) -> CategoriaDocumentoService:
    return service

router = APIRouter(
    prefix="/categorias-documento",
    tags=["Categorias de Documento"]
)

categorias_tag_metadata={
    "name": "Categorias de Documento",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Categoria, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Categoria.",
}

@router.post(
    "",
    response_model=CategoriaDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea una nueva categoria")
async def add_categoria_documento(
    categoria_request: CategoriaDocumentoRequestDTO,
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    return await service.add(categoria_request)


@router.get(
    "",
    response_model=List[CategoriaDocumentoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las categorias")
async def get_all_categorias_documento(
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    return await service.get_all()


@router.get(
    "/search",
    response_model=List[CategoriaDocumentoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca categorias por cadena de búsqueda"
)
async def search_categorias_documento(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar categorias"),
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    return await service.find(search_string)


@router.get(
    "/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene las categorias paginadas"
)
async def get_paginated_categorias_documento(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    return await service.get_paginated(page, page_size)


@router.get(
    "/{categoria_id}",
    response_model=CategoriaDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene una categoria por su ID"
)
async def get_categoria_documento_by_id(
    categoria_id: int,
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    return await service.get_by_id(categoria_id)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza una categoria"
)
async def update_categoria_documento(
    categoria_id: int,
    categoria_request: CategoriaDocumentoRequestDTO,
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    return await service.update(categoria_id, categoria_request)


@router.delete(
    "/{categoria_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina una categoria"
)
async def delete_categoria_documento_by_id(
    categoria_id: int,
    service: CategoriaDocumentoService = Depends(get_categoria_documento_service_imp)
):
    await service.delete_by_id(categoria_id)
    return JSONResponse(
        content={"message": "Se eliminó la categoria correctamente"},
        status_code=200
    )





