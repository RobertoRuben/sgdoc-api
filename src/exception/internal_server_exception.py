from fastapi import status, HTTPException
from typing import Any, Optional

class InternalServerException(HTTPException):
    def __init__(
            self,
            detail: str = "Error interno del servidor",
            error_details: Optional[Any] = None
    ):
        error_response = {
            "error": detail,
            "details": str(error_details) if error_details is not None else None
        }
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response
        )