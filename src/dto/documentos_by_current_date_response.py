from pydantic import BaseModel

class DocumentosByCurrentDateResponse(BaseModel):
    total_documents: int


class TotalDerivedDocumentsToday(BaseModel):
    total_derived_documents_today: int


class TotalPendingDerivedDocumentsToday(BaseModel):
    total_pending_derived_documents_today: int


class TotalDocumentsByCaserioToday(BaseModel):
    nombre_caserio: str
    total_documents: int

