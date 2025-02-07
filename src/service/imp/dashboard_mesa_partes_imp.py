from typing import List
from fastapi import Depends
from src.dto import (
    DocumentosIngresadosResponseDTO,
    TotalDocumentosDerivaodsResponseDTO,
    TotalDocumentosNoDerivadosResponseDTO,
    TotalDocumentosPorCaserioResponseDTO,
)
from src.repository import DashboardMesaPartesRepository
from src.exception import InternalServerException
from src.service import DashboardMesaPartesService


class DashboardMesaPartesServiceImp(DashboardMesaPartesService):
    def __init__(self, documentos_by_current_date_repository: DashboardMesaPartesRepository = Depends()):
        self.documentos_by_current_date_repository = documentos_by_current_date_repository

    async def get_todays_total_documents_received(self) -> DocumentosIngresadosResponseDTO:
        try:
            total_documents = await self.documentos_by_current_date_repository.get_number_documentos_by_current_date()
            return DocumentosIngresadosResponseDTO(
                total_documentos=total_documents
            )
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el número total de documentos de hoy",
                error_details=str(e)
            ) from e


    async def get_todays_total_derived_documents(self) -> TotalDocumentosDerivaodsResponseDTO:
        try:
            total_derived_documents_today = await self.documentos_by_current_date_repository.get_number_documentos_derivados_current_date()
            return TotalDocumentosDerivaodsResponseDTO(
                total_documentos_derivados=total_derived_documents_today
            )
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el número total de documentos derivados de hoy",
                error_details=str(e)
            ) from e


    async def get_todays_total_pending_derived_documents(self) -> TotalDocumentosNoDerivadosResponseDTO:
        try:
            total_pending_derived_documents_today = await self.documentos_by_current_date_repository.get_number_documentos_pendientes_derivar_current_date()
            return TotalDocumentosNoDerivadosResponseDTO(
                total_documentos_no_derivados=total_pending_derived_documents_today
            )
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el número total de documentos pendientes de derivar de hoy",
                error_details=str(e)
            ) from e


    async def get_todays_documents_by_village(self) -> List[TotalDocumentosPorCaserioResponseDTO]:
        try:
            caserios_with_documents_count = await self.documentos_by_current_date_repository.get_caserios_with_documentos_count_current_date()
            return [
                TotalDocumentosPorCaserioResponseDTO(
                    nombre_caserio=caserio,
                    total_documentos_ingresados=total_documents
                )
                for caserio, total_documents in caserios_with_documents_count
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los documentos por caserío de hoy",
                error_details=str(e)
            ) from e
