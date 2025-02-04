from typing import List
from src.schemas.error_detail_response_schema import ErrorDetailResponseSchema
from src.schemas.error_response_schema import ErrorResponseSchema

class ValidationErrorResponseSchema(ErrorResponseSchema):
    details: List[ErrorDetailResponseSchema]