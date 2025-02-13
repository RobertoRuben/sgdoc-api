from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class BadRequestException(AppException):
    def __init__(
        self,
        detail: str = "Solicitud incorrecta",
        error_details: Optional[Any] = None,
        headers: Optional[dict] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_details=error_details,
            headers=headers
        )