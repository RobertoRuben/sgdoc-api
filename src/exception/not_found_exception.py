from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class NotFoundException(AppException):
    def __init__(
        self,
        detail: str = "Recurso no encontrado",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_details=error_details
        )
