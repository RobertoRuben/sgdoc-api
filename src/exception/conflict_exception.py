from fastapi import status
from typing import Any, Optional
from .app_exception import AppException

class ConflictException(AppException):
    def __init__(
        self,
        detail: str = "Conflicto de datos",
        error_details: Optional[Any] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_details=error_details
        )