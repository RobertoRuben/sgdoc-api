from typing import Dict, Any, List
from fastapi import HTTPException, Depends
from src.model.entity.estado_documento import EstadoDocumento
from src.dto.estado_documento_request import EstadoDocumentoRequest
from src.dto.estado_documento_response import EstadoDocumentoResponse
from src.repository.estado_documento_repository import EstadoDocumentoRepository
from src.repository.documento_repository import DocumentoRepository

class EstadoDocumentoService:
    def __init__(self, estado_documento_repository: EstadoDocumentoRepository = Depends(), documento_repository: DocumentoRepository = Depends()):
        self.estado_documento_repository = estado_documento_repository
        self.documento_repository = documento_repository

    def add_estado_documento(self, estado_documento_request: EstadoDocumentoRequest) -> EstadoDocumentoResponse:

        if not self.documento_repository.exists_by_id(estado_documento_request.documento_id):
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        estado_documento = EstadoDocumento(
            estado=estado_documento_request.estado,
            comentario=estado_documento_request.comentario,
            documento_id=estado_documento_request.documento_id
        )

        created_estado_documento = self.estado_documento_repository.add_estado_documento(estado_documento)

        return EstadoDocumentoResponse(
            id=created_estado_documento.id,
            estado=created_estado_documento.estado,
            comentario=created_estado_documento.comentario,
            fecha=created_estado_documento.fecha
        )

    def get_all_estado_documento(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        return self.estado_documento_repository.get_all_estado_documento(page, page_size)


    def update_estado_documento(self, estado_documento_id: int, estado_documento_request: EstadoDocumentoRequest) -> EstadoDocumentoResponse:
        estado_documento = self.estado_documento_repository.get_estado_documento_by_id(estado_documento_id)

        if not self.documento_repository.exists_by_id(estado_documento_request.documento_id):
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        estado_documento.estado = estado_documento_request.estado
        estado_documento.comentario = estado_documento_request.comentario
        estado_documento.documento_id = estado_documento_request.documento_id

        updated_estado_documento = self.estado_documento_repository.update_estado_documento(estado_documento)

        return EstadoDocumentoResponse(
            id=updated_estado_documento.id,
            estado=updated_estado_documento.estado,
            comentario=updated_estado_documento.comentario,
            fecha=updated_estado_documento.fecha
        )


    def delete_documento(self, estado_documento_id: int) -> None:
        if not self.estado_documento_repository.exits_estado_documento_by_id(estado_documento_id):
            raise HTTPException(status_code=404, detail="Estado de documento no encontrado")
        self.estado_documento_repository.delete_by_id(estado_documento_id)


    def get_all_by_id(self, documento_id: int) -> List[EstadoDocumento]:
        return self.estado_documento_repository.get_all_by_id(documento_id)

