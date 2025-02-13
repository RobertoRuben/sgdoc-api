from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class ForbiddenException(AppException):
    def __init__(
        self,
        detail: str = "Acceso prohibido",
        error_details: Optional[Any] = None,
        headers: Optional[dict] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_details=error_details,
            headers=headers
        )