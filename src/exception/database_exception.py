from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class DatabaseException(AppException):
    def __init__(
        self,
        detail: str = "Error en la operación de base de datos",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_details=error_details
        )