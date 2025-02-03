from typing import List
from src.schemas.error_detail_response import ErrorDetailResponse
from src.schemas.error_response import ErrorResponse

class ValidationErrorResponse(ErrorResponse):
    details: List[ErrorDetailResponse]