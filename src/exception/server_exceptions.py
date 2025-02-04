from fastapi import status, HTTPException

class DatabaseException(HTTPException):
    def __init__(self, detail: str = "Error en la operación de base de datos"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class InternalServerException(HTTPException):
    def __init__(self, detail: str = "Error interno del servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )