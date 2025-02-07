from datetime import date
from typing import Optional, Dict, Any, Tuple
from fastapi import Depends
from src.exception import NotFoundException, ConflictException, InternalServerException
from src.model.entity import Documento, Remitente
from src.dto import DocumentoRequestDTO, DocumentoUpdateRequestDTO, DocumentoResponseDTO, RemitenteRequestDTO, DocumentosNoConfirmadosResponseDTO
from src.repository import DocumentoRepository, RemitenteRepository
from src.service import DocumentoService

class DocumentoServiceImp(DocumentoService):
    def __init__(
        self,
        documento_repository: DocumentoRepository = Depends(),
        remitente_repository: RemitenteRepository = Depends()
    ):
        self.documento_repository = documento_repository
        self.remitente_repository = remitente_repository


    async def add(self, remitente_request: RemitenteRequestDTO, documento_request: DocumentoRequestDTO) -> DocumentoResponseDTO:
        try:
            if await self.documento_repository.exists_by_name(documento_request.nombre):
                raise ConflictException("Ya existe un documento con el nombre proporcionado")

            if await self.remitente_repository.exists(remitente_request.dni):
                existing_remitente = await self.remitente_repository.get_by_dni(remitente_request.dni)
                remitente_id = existing_remitente.id
            else:
                new_remitente = Remitente(
                    dni=remitente_request.dni,
                    nombres=remitente_request.nombres,
                    apellido_paterno=remitente_request.apellido_paterno,
                    apellido_materno=remitente_request.apellido_materno,
                    genero=remitente_request.genero
                )
                created_remitente = await self.remitente_repository.add_remitentes(new_remitente)
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

            created_documento = await self.documento_repository.add_documentos(new_documento)

            return DocumentoResponseDTO(
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
        except ConflictException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el documento",
                error_details=str(e)
            ) from e


    async def update(self, documento_id: int, documento_update_request: DocumentoUpdateRequestDTO) -> DocumentoResponseDTO:
        try:
            documento = await self.documento_repository.get_document_by_id(documento_id)
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

            updated_documento = await self.documento_repository.update_document(documento)

            return DocumentoResponseDTO(
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
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el documento",
                error_details=str(e)
            ) from e


    async def delete(self, documento_id: int) -> None:
        try:
            if not await self.documento_repository.exists_by_id(documento_id):
                raise NotFoundException("Documento no encontrado")
            await self.documento_repository.delete_document_by_id(documento_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el documento",
                error_details=str(e)
            ) from e


    async def get_by_id(self, documento_id: int) -> Documento:
        try:
            documento = await self.documento_repository.get_document_by_id(documento_id)
            if not documento:
                raise NotFoundException("Documento no encontrado")
            return documento
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el documento",
                error_details=str(e)
            ) from e


    async def download_by_id(self, documento_id: int) -> Tuple[bytes, str]:
        try:
            if not await self.documento_repository.exists_by_id(documento_id):
                raise NotFoundException("Documento no encontrado")
            documento_bytes, nombre = await self.documento_repository.get_document_bytes_and_name_by_id(documento_id)
            if not documento_bytes or not nombre:
                raise ConflictException("El documento no tiene contenido")
            return documento_bytes, nombre
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al descargar el documento",
                error_details=str(e)
            ) from e


    async def get_paginted_by_current_date(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            return await self.documento_repository.get_documents_by_current_date(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener documentos por fecha actual",
                error_details=str(e)
            ) from e


    async def get_all(self, p_page: int, p_page_size: int) -> Dict[str, Any]:
        try:
            return await self.documento_repository.get_all_documents_paginated(p_page, p_page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener todos los documentos",
                error_details=str(e)
            ) from e


    async def find(
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
        try:
            return await self.documento_repository.search_entered_documents(
                p_page,
                p_page_size,
                p_dni,
                p_id_caserio,
                p_id_centro_poblado,
                p_id_ambito,
                p_nombre_categoria,
                p_fecha_ingreso
            )
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar documentos ingresados",
                error_details=str(e)
            ) from e


    async def get_paginatend_send_by_area_origen_id(
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
        try:
            return await self.documento_repository.get_sent_documents_by_area_id(
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
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener documentos enviados por área origen",
                error_details=str(e)
            ) from e


    async def get_paginated_reject_by_area_destino_id(
        self,
        p_area_destino_id: int,
        p_search_document: Optional[int] = None,
        p_id_caserio: Optional[int] = None,
        p_id_centro_poblado: Optional[int] = None,
        p_id_ambito: Optional[int] = None,
        p_nombre_categoria: Optional[str] = None,
        p_fecha_ingreso: Optional[str] = None,
        p_page: int = 1,
        p_page_size: int = 10
    ) -> Dict[str, Any]:
        try:
            return await self.documento_repository.get_rejected_documents_by_area_id(
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
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener documentos rechazados por área destino",
                error_details=str(e)
            ) from e


    async def get_paginated_receive_by_area_destino_id(
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
        try:
            return await self.documento_repository.get_received_documents_by_area_id(
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
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener documentos recibidos por área destino",
                error_details=str(e)
            ) from e


    async def get_unconfirmed_documents(self, p_area_destino_id: int) -> DocumentosNoConfirmadosResponseDTO:
        try:
            total = await self.documento_repository.get_total_unconfirmed_received_documents_today(p_area_destino_id)
            return DocumentosNoConfirmadosResponseDTO(total=total)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener documentos no confirmados",
                error_details=str(e)
            ) from e
