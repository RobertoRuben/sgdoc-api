from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class InternalServerException(AppException):
    def __init__(
        self,
        detail: str = "Error interno del servidor",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_details=error_details
        )