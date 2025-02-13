from datetime import date
from io import BytesIO
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form, Path
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from src.exception import InternalServerException
from src.schemas import *
from src.exception import  BadRequestException
from src.dto import (
    DocumentoRequestDTO,
    DocumentoResponseDTO,
    DocumentosNoConfirmadosResponseDTO,
    DocumentoUpdateRequestDTO,
    PaginatedResponseDTO,
    RemitenteRequestDTO
)
from src.model.enum import GeneroEnum
from src.service.documento_service import DocumentoService
from src.service.imp import DocumentoServiceImp

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"]
)

documentos_tag_metadata = {
    "name": "Documentos",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Documentos, "
                   "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros de Documentos.",
}


def get_document_service_imp(service: DocumentoServiceImp = Depends()) -> DocumentoService:
    return service

@router.post(
    "",
    response_model=DocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo documento"
)
async def add_documento(
    documento_file: UploadFile = File(..., description="Archivo PDF del documento"),
    dni: int = Form(..., ge=10000000, le=99999999, description="DNI de 8 dígitos"),
    nombres: str = Form(..., min_length=1, description="El nombre no debe estar vacío"),
    apellido_paterno: str = Form(..., min_length=1, description="El apellido paterno no debe estar vacío"),
    apellido_materno: str = Form(..., min_length=1, description="El apellido materno no debe estar vacío"),
    genero: GeneroEnum = Form(..., description="El género debe ser Masculino o Femenino"),
    folios: int = Form(..., ge=1, description="El número de folios debe ser mayor o igual a 1"),
    nombre: str = Form(..., min_length=1, description="El nombre del documento no puede estar vacío"),
    asunto: str = Form(..., min_length=1, description="El asunto no puede estar vacío"),
    ambito_id: int = Form(..., ge=1, description="El id del ámbito debe ser mayor o igual a 1"),
    categoria_id: int = Form(..., ge=1, description="El id de la categoría debe ser mayor o igual a 1"),
    caserio_id: Optional[int] = Form(None, ge=1, description="El id del caserío debe ser mayor o igual a 1 si se proporciona"),
    centro_poblado_id: Optional[int] = Form(None, ge=1, description="El id del centro poblado debe ser mayor o igual a 1 si se proporciona"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    if documento_file.content_type != "application/pdf":
        raise BadRequestException("El archivo debe ser de tipo PDF")

    documento_bytes = await documento_file.read()

    remitente_request = RemitenteRequestDTO(
        dni=dni,
        nombres=nombres,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        genero=genero
    )

    documento_request = DocumentoRequestDTO(
        documento_bytes=documento_bytes,
        folios=folios,
        nombre=nombre,
        asunto=asunto,
        ambito_id=ambito_id,
        categoria_id=categoria_id,
        caserio_id=caserio_id,
        centro_poblado_id=centro_poblado_id
    )
    return await documento_service.add(remitente_request, documento_request)


@router.get(
    "",
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    response_model=PaginatedResponseDTO,
    description="Obtiene todos los documentos"
)
async def get_all_documents(
    p_page: int = 1,
    p_page_size: int = 10,
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_all(p_page, p_page_size)


@router.get(
    "/search",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca documentos según criterios específicos"
)
async def find_documentos(
    p_page: int = Query(1, ge=1, description="Número de página para la paginación"),
    p_page_size: int = Query(10, ge=1, le=100, description="Cantidad de elementos por página"),
    p_dni: Optional[int] = Query(None, ge=1, le=99999999, description="DNI de 8 dígitos para filtrar"),
    p_id_caserio: Optional[int] = Query(None, description="ID del caserío"),
    p_id_centro_poblado: Optional[int] = Query(None, description="ID del centro poblado"),
    p_id_ambito: Optional[int] = Query(None, description="ID del ámbito"),
    p_nombre_categoria: Optional[str] = Query(None, description="Nombre de la categoría"),
    p_fecha_ingreso: Optional[date] = Query(None, description="Fecha de ingreso (YYYY-MM-DD)"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.find(
            p_page=p_page,
            p_page_size=p_page_size,
            p_dni=p_dni,
            p_id_caserio=p_id_caserio,
            p_id_centro_poblado=p_id_centro_poblado,
            p_id_ambito=p_id_ambito,
            p_nombre_categoria=p_nombre_categoria,
            p_fecha_ingreso=p_fecha_ingreso
        )


@router.get(
    "/sends",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene documentos enviados por un área específica con filtros y paginación"
)
async def get_paginated_sent_documents_by_area_id(
    p_area_origen_id: int = Query(..., ge=1, description="ID del área de origen"),
    p_search_document: Optional[str] = Query(None, description="Palabra clave para buscar documentos"),
    p_id_caserio: Optional[int] = Query(None, description="ID del caserío"),
    p_id_centro_poblado: Optional[int] = Query(None, description="ID del centro poblado"),
    p_id_ambito: Optional[int] = Query(None, description="ID del ámbito"),
    p_nombre_categoria: Optional[str] = Query(None, description="Nombre de la categoría"),
    p_fecha_ingreso: Optional[date] = Query(None, description="Fecha de ingreso (YYYY-MM-DD)"),
    p_page: int = Query(1, ge=1, description="Número de página para la paginación"),
    p_page_size: int = Query(10, ge=1, le=100, description="Cantidad de elementos por página"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_paginatend_send_by_area_origen_id(
        p_area_origen_id=p_area_origen_id,
        p_search_document=p_search_document,
        p_id_caserio=p_id_caserio,
        p_id_centro_poblado=p_id_centro_poblado,
        p_id_ambito=p_id_ambito,
        p_nombre_categoria=p_nombre_categoria,
        p_fecha_ingreso=p_fecha_ingreso,
        p_page=p_page,
        p_page_size=p_page_size
    )


@router.get(
    "/received",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene documentos recibidos por un área específica con filtros y paginación"
)
async def get_paginated_received_documents_by_area_id(
    p_area_destino_id: int = Query(..., ge=1, description="ID del área de destino"),
    p_search_document: Optional[str] = Query(None, description="Palabra clave para buscar documentos"),
    p_id_caserio: Optional[int] = Query(None, description="ID del caserío"),
    p_id_centro_poblado: Optional[int] = Query(None, description="ID del centro poblado"),
    p_id_ambito: Optional[int] = Query(None, description="ID del ámbito"),
    p_nombre_categoria: Optional[str] = Query(None, description="Nombre de la categoría"),
    p_fecha_ingreso: Optional[str] = Query(None, description="Fecha de ingreso (YYYY-MM-DD)"),
    p_page: int = Query(1, ge=1, description="Número de página para la paginación"),
    p_page_size: int = Query(10, ge=1, le=100, description="Cantidad de elementos por página"),
    p_recepcionada: Optional[bool] = Query(None, description="Filtrar por confirmación (recepcionada)"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_paginated_receive_by_area_destino_id(
        p_area_destino_id=p_area_destino_id,
        p_search_document=p_search_document,
        p_id_caserio=p_id_caserio,
        p_id_centro_poblado=p_id_centro_poblado,
        p_id_ambito=p_id_ambito,
        p_nombre_categoria=p_nombre_categoria,
        p_fecha_ingreso=p_fecha_ingreso,
        p_page=p_page,
        p_page_size=p_page_size,
        p_recepcionada=p_recepcionada
    )


@router.get(
    "/rejected",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene documentos recibidos por un área específica con filtros y paginación"
)
async def get_paginated_rejected_documents_by_area_id(
    p_area_destino_id: int = Query(..., ge=1, description="ID del área de destino"),
    p_search_document: Optional[str] = Query(None, description="Palabra clave para buscar documentos"),
    p_id_caserio: Optional[int] = Query(None, description="ID del caserío"),
    p_id_centro_poblado: Optional[int] = Query(None, description="ID del centro poblado"),
    p_id_ambito: Optional[int] = Query(None, description="ID del ámbito"),
    p_nombre_categoria: Optional[str] = Query(None, description="Nombre de la categoría"),
    p_fecha_ingreso: Optional[str] = Query(None, description="Fecha de ingreso (YYYY-MM-DD)"),
    p_page: int = Query(1, ge=1, description="Número de página para la paginación"),
    p_page_size: int = Query(10, ge=1, le=100, description="Cantidad de elementos por página"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_paginated_reject_by_area_destino_id(
        p_area_destino_id=p_area_destino_id,
        p_search_document=p_search_document,
        p_id_caserio=p_id_caserio,
        p_id_centro_poblado=p_id_centro_poblado,
        p_id_ambito=p_id_ambito,
        p_nombre_categoria=p_nombre_categoria,
        p_fecha_ingreso=p_fecha_ingreso,
        p_page=p_page,
        p_page_size=p_page_size
    )


@router.get(
    "/entered-current-date",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene los documentos ingresados en la fecha actual"
)
async def get_paginated_entered_documents_by_current_date(
    page: int = 1,
    page_size: int = 10,
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_paginted_by_current_date(page, page_size)


@router.get(
    "/unconfirmed",
    response_model=DocumentosNoConfirmadosResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos no confirmados recibidos hoy por un área de destino específica"
)
async def get_unconfirmed_documentos(
    p_area_destino_id: int = Query(..., ge=1, description="ID del área de destino"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_unconfirmed_documents(p_area_destino_id)


@router.get(
    "/{documento_id}",
    response_model=DocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un documento por su ID"
)
async def get_documento_by_id(
    documento_id: int,
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    return await documento_service.get_by_id(documento_id)


@router.put(
    "/{documento_id}",
    response_model=DocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un documento existente"
)
async def update_documento(
    documento_id: int = Path(..., ge=1, description="ID del documento a actualizar"),
    documento_file: Optional[UploadFile] = File(None,description="Archivo PDF del documento (opcional)"),
    folios: int = Form(..., ge=1, description="El número de folios debe ser mayor o igual a 1"),
    nombre: str = Form(..., min_length=1, description="El nombre del documento no puede estar vacío"),
    asunto: str = Form(..., min_length=1, description="El asunto no puede estar vacío"),
    ambito_id: int = Form(..., ge=1, description="El id del ámbito debe ser mayor o igual a 1"),
    categoria_id: int = Form(..., ge=1, description="El id de la categoría debe ser mayor o igual a 1"),
    caserio_id: Optional[int] = Form(None, ge=1, description="El id del caserío debe ser mayor o igual a 1 si se proporciona"),
    centro_poblado_id: Optional[int] = Form(None, ge=1, description="El id del centro poblado debe ser mayor o igual a 1 si se proporciona"),
    documento_service: DocumentoService = Depends(get_document_service_imp)
):
    documento_bytes = None
    if documento_file:
        if documento_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="El archivo debe ser de tipo PDF")
        documento_bytes = await documento_file.read()

    documento_request = DocumentoUpdateRequestDTO(
        documento_bytes=documento_bytes,
        folios=folios,
        nombre=nombre,
        asunto=asunto,
        ambito_id=ambito_id,
        categoria_id=categoria_id,
        caserio_id=caserio_id,
        centro_poblado_id=centro_poblado_id
    )

    return await documento_service.update(documento_id, documento_request)


@router.delete(
    "/{documento_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un documento por su ID"
)
async def delete_documento_by_id(
    documento_id: int,
    documento_service: DocumentoServiceImp = Depends(get_document_service_imp)
):
    await documento_service.delete(documento_id)
    return JSONResponse(
        content={"message": "Se eliminó el documento correctamente"},
        status_code=200
    )


@router.get(
    "/{documento_id}/download",
    response_model=FileDownloadResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Descarga el documento por su ID"
)
async def download_documento_by_id(documento_id: int, documento_service: DocumentoServiceImp = Depends()):
    try:
        documento_bytes, nombre = documento_service.download_by_id(documento_id)

        file_like = BytesIO(documento_bytes)

        headers = {
            "Content-Disposition": f'attachment; filename="{nombre}.pdf"'
        }
        return StreamingResponse(file_like, media_type="application/pdf", headers=headers)
    except Exception as e:
        raise InternalServerException(
            detail="Error al descargar el documento",
            error_details=str(e)
        ) from e





