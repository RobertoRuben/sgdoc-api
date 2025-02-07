from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import UsuarioRequestDTO, UsuarioResponseDTO

class UsuarioService(ABC):
    @abstractmethod
    async def add(self, usuario_request: UsuarioRequestDTO) -> UsuarioResponseDTO:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int, is_active: bool) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, usuario_id: int, usuario_request: UsuarioRequestDTO) -> UsuarioResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, usuario_id: int) -> None:
        pass

    @abstractmethod
    async def update_status(self, usuario_id: int, active: bool) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[UsuarioRequestDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, usuario_id: int) -> UsuarioResponseDTO:
        pass

    @abstractmethod
    async def update_password(self, usuario_id: int, contrasena: str) -> None:
        pass
