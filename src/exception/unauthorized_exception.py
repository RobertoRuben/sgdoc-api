from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class UnauthorizedException(AppException):
    def __init__(
        self,
        detail: str = "No autorizado",
        error_details: Optional[Any] = None,
        headers: Optional[dict] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_details=error_details,
            headers=headers
        )