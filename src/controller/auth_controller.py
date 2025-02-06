from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.security.dependencies import get_current_user
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema
from typing import Annotated
from src.dto.auth_request_dto import AuthRequestDTO
from src.dto.auth_response_dto import AuthResponseDTO
from src.dto.refresh_token import RefreshTokenRequest
from src.dto.user_info_response import UserInfoResponse
from src.service.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/login",
    response_model=AuthResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends()
) -> AuthResponseDTO:
    auth_request = AuthRequestDTO(
        username=form_data.username,
        password=form_data.password
    )
    return auth_service.authenticate_user(auth_request)


@router.get(
    "/me",
    response_model=UserInfoResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
)
def read_users_me(current_user = Depends(get_current_user)):
    user, trabajador, rol = current_user

    return UserInfoResponse(
        id=user.id,
        username=user.nombre_usuario,
        rol_id=user.rol_id,
        rol_name=rol.nombre_rol,
        is_active=user.is_active,
        area_id=trabajador.area_id
    )


@router.post(
    "/refresh",
    response_model=AuthResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
)
def refresh_token(
    req: RefreshTokenRequest,
    auth_service: AuthService = Depends()
):
    return auth_service.refresh_access_token(req.refresh_token)

