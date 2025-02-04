from fastapi import status, HTTPException

class BadRequestException(HTTPException):
    def __init__(self, detail: str, headers: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers
        )

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, headers: dict = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers
        )

class ForbiddenException(HTTPException):
    def __init__(self, detail: str, headers: dict = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers=headers
        )

class NotFoundException(HTTPException):
    def __init__(self, detail: str, headers: dict = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers
        )

class ConflictException(HTTPException):
    def __init__(self, detail: str, headers: dict = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers=headers
        )