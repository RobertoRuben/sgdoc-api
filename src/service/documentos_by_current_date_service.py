from typing import List

from fastapi import Depends
from src.dto.documentos_by_current_date_response import DocumentosByCurrentDateResponse, TotalDerivedDocumentsToday, TotalPendingDerivedDocumentsToday, TotalDocumentsByCaserioToday
from src.repository.documentos_by_current_date_repository import DocumentosByCurrentDateRepository

class DocumentsByCurrentDateService:

    def __init__(self, documentos_by_current_date_repository: DocumentosByCurrentDateRepository = Depends()):
        self.documentos_by_current_date_repository = documentos_by_current_date_repository


    def get_total_number_documents_today(self) -> DocumentosByCurrentDateResponse:
        total_documents = self.documentos_by_current_date_repository.get_number_documentos_by_current_date()
        return DocumentosByCurrentDateResponse(total_documents=total_documents)


    def get_total_number_derived_documents_today(self) -> TotalDerivedDocumentsToday:
        total_derived_documents_today = self.documentos_by_current_date_repository.get_number_documentos_derivados_current_date()
        return TotalDerivedDocumentsToday(total_derived_documents_today=total_derived_documents_today)


    def get_total_number_pending_derived_documents_today(self) -> TotalPendingDerivedDocumentsToday:
        total_pending_derived_documents_today = self.documentos_by_current_date_repository.get_number_documentos_pendientes_derivar_current_date()
        return TotalPendingDerivedDocumentsToday(total_pending_derived_documents_today=total_pending_derived_documents_today)


    def get_total_documents_by_caserio_today(self) -> List[TotalDocumentsByCaserioToday]:
        caserios_with_documents_count = self.documentos_by_current_date_repository.get_caserios_with_documentos_count_current_date()
        return [TotalDocumentsByCaserioToday(nombre_caserio=caserio, total_documents=total_documents) for caserio, total_documents in caserios_with_documents_count]

