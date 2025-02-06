from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto.ambito_request import AmbitoRequest
from src.dto.ambito_response import AmbitoResponse

class AmbitoService(ABC):

    @abstractmethod
    async def add_ambito(self, ambito_request: AmbitoRequest) -> AmbitoResponse:
        pass

    @abstractmethod
    async def get_all_ambitos(self) -> List[AmbitoResponse]:
        pass

    @abstractmethod
    async def update_ambito(self, ambito_id: int, ambito_request: AmbitoRequest) -> AmbitoResponse:
        pass

    @abstractmethod
    async def delete_ambito(self, ambito_id: int) -> None:
        pass

    @abstractmethod
    async def find_ambito(self, search_string: str) -> List[AmbitoResponse]:
        pass

    @abstractmethod
    async def get_ambitos_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_ambito_by_id(self, ambito_id: int) -> AmbitoResponse:
        pass
