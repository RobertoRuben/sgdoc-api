from abc import ABC, abstractmethod
from src.dto import AuthRequestDTO, AuthResponseDTO

class AuthService(ABC):
    @abstractmethod
    async def authenticate_user(self, auth_request: AuthRequestDTO) -> AuthResponseDTO:
        pass

    @abstractmethod
    async def refresh_access_token(self, refresh_token: str) -> AuthResponseDTO:
        pass

    @abstractmethod
    def get_username_from_token(self, token: str) -> str:
        pass
