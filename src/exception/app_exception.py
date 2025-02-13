from fastapi import HTTPException
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_details: Optional[Any] = None,
        headers: Optional[dict] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": detail,
                "details": str(error_details) if error_details else None
            },
            headers=headers
        )
        logger.error(f"{self.__class__.__name__}: {detail} - {error_details}")