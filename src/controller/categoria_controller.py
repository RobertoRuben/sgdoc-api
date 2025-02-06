from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema, DeleteSuccessfulResponseSchema
from src.service.imp.categoria_documento_service_imp import CategoriaDocumentoServiceImp
from src.dto.categoria_documento_request_dto import CategoriaDocumentoRequestDTO
from src.dto.categoria_documento_response_dto import CategoriaDocumentoResponseDTO
from src.dto.paginated_response import PaginatedResponseDTO

router = APIRouter(tags=["Categorias"])

categorias_tag_metadata={
    "name": "Categorias",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Categoria, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Categoria.",
}

@router.post(
    "/categorias",
    response_model=CategoriaDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea una nueva categoria")
async def add_categoria(categoria_request: CategoriaDocumentoRequestDTO, service: CategoriaDocumentoServiceImp = Depends()):
    return service.add_categoria_documento(categoria_request)


@router.get(
    "/categorias",
    response_model=List[CategoriaDocumentoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las categorias")
async def get_categorias(service: CategoriaDocumentoServiceImp = Depends()):
    return service.get_all_categorias_documento()


@router.get(
    "/categorias/search",
    response_model=List[CategoriaDocumentoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca categorias por cadena de búsqueda"
)
async def search_categorias(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar categorias"),
    service: CategoriaDocumentoServiceImp = Depends()
):
    return service.find_categoria_documento(search_string)


@router.get(
    "/categorias/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene las categorias paginadas"
)
async def get_paginated_categorias(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: CategoriaDocumentoServiceImp = Depends()
):
    return service.get_categorias_documento_paginated(page, page_size)


@router.get(
    "/categorias/{categoria_id}",
    response_model=CategoriaDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene una categoria por su ID"
)
async def get_categoria_by_id(categoria_id: int, service: CategoriaDocumentoServiceImp = Depends()):
    return service.get_categoria_documento_by_id(categoria_id)


@router.put(
    "/categorias/{categoria_id}",
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
async def update_categoria(categoria_id: int, categoria_request: CategoriaDocumentoRequestDTO, service: CategoriaDocumentoServiceImp = Depends()):
    return service.update_categoria_documento(categoria_id, categoria_request)


@router.delete(
    "/categorias/{categoria_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina una categoria"
)
async def delete_categoria(categoria_id: int, service: CategoriaDocumentoServiceImp = Depends()):
    service.delete_categoria_documento_by_id(categoria_id)
    return JSONResponse(content={"message": "Se eliminó la categoria correctamente"}, status_code=200)





