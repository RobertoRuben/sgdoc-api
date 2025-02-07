from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Dict, Any, Tuple
from src.dto.documento_request_dto import DocumentoRequestDTO
from src.dto.documento_response_dto import DocumentoResponseDTO, DocumentosNoConfirmadosResponseDTO
from src.dto.documento_update_request_dto import DocumentoUpdateRequestDTO
from src.dto.remitente_request_dto import RemitenteRequestDTO
from src.model.entity.documento import Documento

class DocumentoService(ABC):

    @abstractmethod
    async def add(self, remitente_request: RemitenteRequestDTO, documento_request: DocumentoRequestDTO) -> DocumentoResponseDTO:
        pass

    @abstractmethod
    async def update(self, documento_id: int, documento_update_request: DocumentoUpdateRequestDTO) -> DocumentoResponseDTO:
        pass

    @abstractmethod
    async def delete(self, documento_id: int) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, documento_id: int) -> Documento:
        pass

    @abstractmethod
    async def download_by_id(self, documento_id: int) -> Tuple[bytes, str]:
        pass

    @abstractmethod
    async def get_paginted_by_current_date(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_all(self, p_page: int, p_page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_unconfirmed_documents(self, p_area_destino_id: int) -> DocumentosNoConfirmadosResponseDTO:
        pass
