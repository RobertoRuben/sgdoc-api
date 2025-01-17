from typing import List

from  fastapi import APIRouter, HTTPException, Depends
from src.dto.documentos_by_current_date_response import DocumentosByCurrentDateResponse, TotalDerivedDocumentsToday, TotalPendingDerivedDocumentsToday, TotalDocumentsByCaserioToday
from src.service.documentos_by_current_date_service import DocumentsByCurrentDateService

router = APIRouter(tags=["Documentos por fecha actual"])

documentos_by_current_date_tag_metadata={
    "name": "Documentos por fecha actual",
    "description": "Esta sección proporciona los endpoints para obtener la cantidad de documentos, documentos derivados y documentos pendientes de derivar en la fecha actual.",
}

@router.get("/documentos-by-current-date", response_model=DocumentosByCurrentDateResponse, description="Obtiene la cantidad de documentos ingresados en la fecha actual")
async def get_total_number_documents_today(service: DocumentsByCurrentDateService = Depends()):
    try:
        return service.get_total_number_documents_today()
    except HTTPException as e:
        raise e


@router.get("/documentos-by-current-date/derived", response_model=TotalDerivedDocumentsToday, description="Obtiene la cantidad de documentos derivados en la fecha actual")
async def get_total_number_derived_documents_today(service: DocumentsByCurrentDateService = Depends()):
    try:
        return service.get_total_number_derived_documents_today()
    except HTTPException as e:
        raise e


@router.get("/documentos-by-current-date/pending-derived", response_model=TotalPendingDerivedDocumentsToday, description="Obtiene la cantidad de documentos pendientes de derivar en la fecha actual")
async def get_total_number_pending_derived_documents_today(service: DocumentsByCurrentDateService = Depends()):
    try:
        return service.get_total_number_pending_derived_documents_today()
    except HTTPException as e:
        raise e


@router.get("/documentos-by-current-date/caserios", response_model=List[TotalDocumentsByCaserioToday], description="Obtiene la cantidad de documentos ingresados en la fecha actual por caserío")
async def get_total_documents_by_caserio_today(service: DocumentsByCurrentDateService = Depends()):
    try:
        return service.get_total_documents_by_caserio_today()
    except HTTPException as e:
        raise e