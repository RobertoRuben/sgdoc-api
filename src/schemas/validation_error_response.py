from typing import List
from src.schemas.error_detail import ErrorDetail
from src.schemas.error_response import ErrorResponse

class ValidationErrorResponse(ErrorResponse):
    details: List[ErrorDetail]