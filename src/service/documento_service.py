from datetime import date
from typing import Optional, Dict, Any
from fastapi import Depends
from src.exception import NotFoundException, ConflictException
from src.model.entity.documento import Documento
from src.model.entity.remitente import Remitente
from src.dto.documento_request import DocumentoRequest
from src.dto.documento_response import DocumentoResponse, DocumentosNoConfirmadosResponseDTO
from src.dto.documento_update_request import DocumentoUpdateRequest
from src.dto.remitente_request import RemitenteRequest
from src.repository.documento_repository import DocumentoRepository
from src.repository.remitente_repository import RemitenteRepository

class DocumentoService:

    def __init__(self, documento_repository: DocumentoRepository = Depends(), remitente_repository: RemitenteRepository = Depends()):
        self.documento_repository = documento_repository
        self.remitente_repository = remitente_repository


    def add_documento(self, remitente_request: RemitenteRequest, documento_request: DocumentoRequest) -> DocumentoResponse:
        if self.documento_repository.exists_by_name(documento_request.nombre):
            raise ConflictException("Ya existe un documento con el nombre proporcionado")

        if self.remitente_repository.exists(remitente_request.dni):
            existing_remitente = self.remitente_repository.get_by_dni(remitente_request.dni)
            remitente_id = existing_remitente.id
        else:
            new_remitente = Remitente(
                dni=remitente_request.dni,
                nombres=remitente_request.nombres,
                apellido_paterno=remitente_request.apellido_paterno,
                apellido_materno=remitente_request.apellido_materno,
                genero=remitente_request.genero
            )
            created_remitente = self.remitente_repository.add_remitentes(new_remitente)
            remitente_id = created_remitente.id

        new_documento = Documento(
            documento_bytes=documento_request.documento_bytes,
            remitente_id=remitente_id,
            folios=documento_request.folios,
            asunto=documento_request.asunto,
            ambito_id=documento_request.ambito_id,
            categoria_id=documento_request.categoria_id,
            caserio_id=documento_request.caserio_id,
            centro_poblado_id=documento_request.centro_poblado_id,
            nombre=documento_request.nombre
        )

        created_documento = self.documento_repository.add_documentos(new_documento)

        return DocumentoResponse(
            id=created_documento.id,
            folios=created_documento.folios,
            nombre=created_documento.nombre,
            asunto=created_documento.asunto,
            remitente_id=created_documento.remitente_id,
            categoria_id=created_documento.categoria_id,
            ambito_id=created_documento.ambito_id,
            caserio_id=created_documento.caserio_id,
            centro_poblado_id=created_documento.centro_poblado_id,
            fecha_ingreso=created_documento.fecha_ingreso
        )


    def update_documento(self, documento_id: int, documento_update_request: DocumentoUpdateRequest) -> DocumentoResponse:
        documento = self.documento_repository.get_document_by_id(documento_id)

        if not documento:
            raise NotFoundException("Documento no encontrado")

        if documento_update_request.documento_bytes is not None:
            documento.documento_bytes = documento_update_request.documento_bytes

        documento.folios = documento_update_request.folios
        documento.nombre = documento_update_request.nombre
        documento.asunto = documento_update_request.asunto
        documento.categoria_id = documento_update_request.categoria_id
        documento.ambito_id = documento_update_request.ambito_id
        documento.caserio_id = documento_update_request.caserio_id
        documento.centro_poblado_id = documento_update_request.centro_poblado_id

        updated_documento = self.documento_repository.update_document(documento)

        return DocumentoResponse(
            id=updated_documento.id,
            folios=updated_documento.folios,
            nombre=updated_documento.nombre,
            asunto=updated_documento.asunto,
            remitente_id=updated_documento.remitente_id,
            categoria_id=updated_documento.categoria_id,
            ambito_id=updated_documento.ambito_id,
            caserio_id=updated_documento.caserio_id,
            centro_poblado_id=updated_documento.centro_poblado_id,
            fecha_ingreso=updated_documento.fecha_ingreso
        )


    def delete_document(self, documento_id: int) -> None:
        if not self.documento_repository.exists_by_id(documento_id):
            raise NotFoundException("Documento no encontrado")

        self.documento_repository.delete_document_by_id(documento_id)


    def get_document_by_id(self, documento_id: int) -> Documento:
        documento = self.documento_repository.get_document_by_id(documento_id)
        if not documento:
            raise NotFoundException("Documento no encontrado")
        return documento


    def descargar_documento(self, documento_id: int) -> tuple[bytes, str]:
        if not self.documento_repository.exists_by_id(documento_id):
            raise NotFoundException("Documento no encontrado")

        documento_bytes, nombre = self.documento_repository.get_document_bytes_and_name_by_id(documento_id)

        if not documento_bytes or not nombre:
            raise ConflictException("El documento no tiene contenido")

        return documento_bytes, nombre


    def get_documentos_by_current_date(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        return self.documento_repository.get_documents_by_current_date(page, page_size)


    def get_all_documents(self, p_page: int, p_page_size: int) -> Dict[str, Any]:
        return self.documento_repository.get_all_documents_paginated(p_page, p_page_size)


    def search_entered_documents(
            self,
            p_page: int,
            p_page_size: int,
            p_dni: int,
            p_id_caserio: int,
            p_id_centro_poblado: int,
            p_id_ambito: int,
            p_nombre_categoria: str,
            p_fecha_ingreso: date
    ) -> Dict[str, Any]:
        return self.documento_repository.search_entered_documents(
            p_page,
            p_page_size,
            p_dni,
            p_id_caserio,
            p_id_centro_poblado,
            p_id_ambito,
            p_nombre_categoria,
            p_fecha_ingreso
        )


    def get_sent_documents_by_area_id(
            self,
            p_area_origen_id: int,
            p_search_document: Optional[int] = None,
            p_id_caserio: Optional[int] = None,
            p_id_centro_poblado: Optional[int] = None,
            p_id_ambito: Optional[int] = None,
            p_nombre_categoria: Optional[str] = None,
            p_fecha_ingreso: Optional[str] = None,
            p_page: int = 1,
            p_page_size: int = 10
    ) -> Dict[str, Any]:
        return self.documento_repository.get_sent_documents_by_area_id(
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


    def get_rejected_documents_by_area_id(
            self,
            p_area_destino_id: int,
            p_search_document: Optional[int] = None,
            p_id_caserio: Optional[int] = None,
            p_id_centro_poblado: Optional[int] = None,
            p_id_ambito: Optional[int] = None,
            p_nombre_categoria: Optional[str] = None,
            p_fecha_ingreso: Optional[str] = None,
            p_page: int = 1,
            p_page_size: int = 10,
    ) -> Dict[str, Any]:
        return self.documento_repository.get_rejected_documents_by_area_id(
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


    def get_received_documents_by_area_id(
            self,
            p_area_destino_id: int,
            p_search_document: Optional[int] = None,
            p_id_caserio: Optional[int] = None,
            p_id_centro_poblado: Optional[int] = None,
            p_id_ambito: Optional[int] = None,
            p_nombre_categoria: Optional[str] = None,
            p_fecha_ingreso: Optional[str] = None,
            p_page: int = 1,
            p_page_size: int = 10,
            p_recepcionada: Optional[bool] = None
    ) -> Dict[str, Any]:
        return self.documento_repository.get_received_documents_by_area_id(
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


    def get_documentos_no_confirmados(self, p_area_destino_id: int) -> DocumentosNoConfirmadosResponseDTO:
        total = self.documento_repository.get_total_unconfirmed_received_documents_today(p_area_destino_id)
        return DocumentosNoConfirmadosResponseDTO(total=total)
