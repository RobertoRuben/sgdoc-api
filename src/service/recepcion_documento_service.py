from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, Depends
from src.model.entity.recepcion_documento import RecepcionDocumento
from src.dto.recepcion_documento_request import RecepcionDocumentoRequest
from src.dto.recepcion_documento_response import RecepcionDocumentoResponse
from src.repository.recepcion_documento_repository import RecepcionDocumentoRepository
from src.repository.documento_repository import DocumentoRepository
from src.repository.usuario_repository import UsuarioRepository

class RecepcionDocumentoService:
    def __init__(self,
                 recepcion_repository: RecepcionDocumentoRepository = Depends(),
                 documento_repository: DocumentoRepository = Depends(),
                 usuario_repository: UsuarioRepository = Depends()):
        self.recepcion_repository = recepcion_repository
        self.documento_repository = documento_repository
        self.usuario_repository = usuario_repository


    def add_recepcion_documento(self, recepcion_documento_request: RecepcionDocumentoRequest) -> RecepcionDocumentoResponse:
        if not self.documento_repository.exists_by_id(recepcion_documento_request.documento_id):
            raise HTTPException(status_code=404, detail="No existe un documento con ese ID")

        if not self.usuario_repository.exists_by_id(recepcion_documento_request.usuario_id):
            raise HTTPException(status_code=404, detail="No existe un usuario con ese ID")

        new_received_document = RecepcionDocumento(
            documento_id=recepcion_documento_request.documento_id,
            fecha_recepcion=datetime.now(),
            usuario_id=recepcion_documento_request.usuario_id
        )

        created_received_document = self.recepcion_repository.add_received_document(new_received_document)

        return RecepcionDocumentoResponse(
            id=created_received_document.id,
            documento_id=created_received_document.documento_id,
            fecha_recepcion=created_received_document.fecha_recepcion,
            usuario_id=created_received_document.usuario_id
        )

    def get_all_recepcion_documento_paginated(self, page: int, size: int) -> Dict[str, Any]:
        return self.recepcion_repository.get_all_paginated(page, size)


    def update_recepcion_documento(self, recepcion_id: int, recepcion_documento_request: RecepcionDocumentoRequest) -> RecepcionDocumentoResponse:
        if not self.recepcion_repository.exists_by_id(recepcion_id):
            raise HTTPException(status_code=404, detail="No existe una recepcion de documento con ese ID")

        if not self.documento_repository.exists_by_id(recepcion_documento_request.documento_id):
            raise HTTPException(status_code=404, detail="No existe un documento con ese ID")

        if not self.usuario_repository.exists_by_id(recepcion_documento_request.usuario_id):
            raise HTTPException(status_code=404, detail="No existe un usuario con ese ID")

        updated_received_document = RecepcionDocumento(
            documento_id=recepcion_documento_request.documento_id,
            fecha_recepcion=datetime.now(),
            usuario_id=recepcion_documento_request.usuario_id
        )

        updated_received_document = self.recepcion_repository.update_received_document(updated_received_document)

        return RecepcionDocumentoResponse(
            id=updated_received_document.id,
            documento_id=updated_received_document.documento_id,
            fecha_recepcion=updated_received_document.fecha_recepcion,
            usuario_id=updated_received_document.usuario_id
        )


    def delete_recepcion_documento(self, recepcion_id: int) -> None:
        if not self.recepcion_repository.exists_by_id(recepcion_id):
            raise HTTPException(status_code=404, detail="No existe una recepcion de documento con ese ID")

        self.recepcion_repository.delete_received_document_by_id(recepcion_id)




