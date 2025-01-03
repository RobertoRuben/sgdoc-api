from datetime import date
from typing import List, Optional
from io import BytesIO
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form, Path
from starlette.responses import StreamingResponse
from src.dto.documento_request import DocumentoRequest
from src.dto.documento_update_request import DocumentoUpdateRequest
from src.dto.documento_response import DocumentoResponse
from src.dto.remitente_request import RemitenteRequest
from src.dto.pagination_response import PaginatedResponse
from src.service.documento_service import DocumentoService
from src.model.enum.genero_enum import GeneroEnum

router = APIRouter(tags=["Documentos"])
documentos_tag_metadata = {
    "name": "Documentos",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Documentos, "
                   "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros de Documentos.",
}

@router.post("/documentos", response_model=DocumentoResponse, description="Crea un nuevo documento")
async def create_documento(
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

    documento_service: DocumentoService = Depends()
):
    try:
        if documento_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="El archivo debe ser de tipo PDF")

        documento_bytes = await documento_file.read()

        remitente_request = RemitenteRequest(
            dni=dni,
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            genero=genero
        )

        documento_request = DocumentoRequest(
            documento_bytes=documento_bytes,
            folios=folios,
            nombre=nombre,
            asunto=asunto,
            ambito_id=ambito_id,
            categoria_id=categoria_id,
            caserio_id=caserio_id,
            centro_poblado_id=centro_poblado_id
        )

        created_documento = documento_service.add_documento(remitente_request, documento_request)
        return created_documento
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/documentos/buscar",
    response_model=PaginatedResponse,
    description="Busca documentos según criterios específicos"
)
async def search_entered_documents(
    p_page: int = Query(1, ge=1, description="Número de página para la paginación"),
    p_page_size: int = Query(10, ge=1, le=100, description="Cantidad de elementos por página"),
    p_dni: Optional[int] = Query(None, ge=10000000, le=99999999, description="DNI de 8 dígitos para filtrar"),
    p_nombre_caserio: Optional[str] = Query(None, description="Nombre del caserío"),
    p_nombre_centro_poblado: Optional[str] = Query(None, description="Nombre del centro poblado"),
    p_nombre_ambito: Optional[str] = Query(None, description="Nombre del ámbito"),
    p_nombre_categoria: Optional[str] = Query(None, description="Nombre de la categoría"),
    p_fecha_ingreso: Optional[date] = Query(None, description="Fecha de ingreso (YYYY-MM-DD)"),
    documento_service: DocumentoService = Depends()
):
    try:
        resultados = documento_service.search_entered_documents(
            p_page=p_page,
            p_page_size=p_page_size,
            p_dni=p_dni,
            p_nombre_caserio=p_nombre_caserio,
            p_nombre_centro_poblado=p_nombre_centro_poblado,
            p_nombre_ambito=p_nombre_ambito,
            p_nombre_categoria=p_nombre_categoria,
            p_fecha_ingreso=p_fecha_ingreso
        )
        return resultados
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/documentos/{documento_id}",
    response_model=DocumentoResponse,
    description="Actualiza un documento existente"
)
async def update_documento(
    documento_id: int = Path(..., ge=1, description="ID del documento a actualizar"),

    documento_file: Optional[UploadFile] = File(
        None,
        description="Archivo PDF del documento (opcional)"
    ),

    folios: int = Form(..., ge=1, description="El número de folios debe ser mayor o igual a 1"),
    nombre: str = Form(..., min_length=1, description="El nombre del documento no puede estar vacío"),
    asunto: str = Form(..., min_length=1, description="El asunto no puede estar vacío"),
    ambito_id: int = Form(..., ge=1, description="El id del ámbito debe ser mayor o igual a 1"),
    categoria_id: int = Form(..., ge=1, description="El id de la categoría debe ser mayor o igual a 1"),
    caserio_id: Optional[int] = Form(None, ge=1, description="El id del caserío debe ser mayor o igual a 1 si se proporciona"),
    centro_poblado_id: Optional[int] = Form(None, ge=1, description="El id del centro poblado debe ser mayor o igual a 1 si se proporciona"),

    documento_service: DocumentoService = Depends()
):
    try:
        documento_bytes = None
        if documento_file:
            if documento_file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="El archivo debe ser de tipo PDF")
            documento_bytes = await documento_file.read()

        documento_request = DocumentoUpdateRequest(
            documento_bytes=documento_bytes,
            folios=folios,
            nombre=nombre,
            asunto=asunto,
            ambito_id=ambito_id,
            categoria_id=categoria_id,
            caserio_id=caserio_id,
            centro_poblado_id=centro_poblado_id
        )

        updated_documento = documento_service.update_documento(documento_id, documento_request)
        return updated_documento

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documentos/{documento_id}", description="Elimina un documento por su ID")
async def delete_documento(
    documento_id: int,
    documento_service: DocumentoService = Depends()
):
    try:
        documento_service.delete_document(documento_id)
        return {"message": "Documento eliminado correctamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documentos/{documento_id}/descargar", description="Descarga el documento por su ID")
async def descargar_documento(
        documento_id: int,
        documento_service: DocumentoService = Depends()
):
    documento_bytes, nombre = documento_service.descargar_documento(documento_id)

    file_like = BytesIO(documento_bytes)

    headers = {
        "Content-Disposition": f'attachment; filename="{nombre}.pdf"'
    }

    return StreamingResponse(file_like, media_type="application/pdf", headers=headers)


@router.get("/documentos/fecha_actual", response_model=PaginatedResponse, description="Obtiene los documentos con fecha actual")
async def get_documents_by_current_date(
        page: int = 1,
        page_size: int = 10,
        documento_service: DocumentoService = Depends()
):
    try:
        return documento_service.get_documentos_by_current_date(page, page_size)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


