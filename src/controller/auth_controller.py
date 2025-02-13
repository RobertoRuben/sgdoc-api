from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.security.dependencies import get_current_user
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema
from src.dto import AuthRequestDTO, AuthResponseDTO, RefreshTokenRequestDTO, AuthenticatedUserResponseDTO
from src.service import AuthService
from src.service.imp import AuthServiceImp

def get_auth_service_imp(service: AuthServiceImp = Depends()) -> AuthService:
    return service

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
async def login_for_access_token(  # Añadir async aquí
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service_imp)
) -> AuthResponseDTO:
    auth_request = AuthRequestDTO(
        username=form_data.username,
        password=form_data.password
    )
    return await auth_service.authenticate_user(auth_request)


@router.get(
    "/me",
    response_model=AuthenticatedUserResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
)
async def read_users_me(current_user = Depends(get_current_user)):
    user, trabajador, rol = current_user

    return AuthenticatedUserResponseDTO(
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
async def refresh_token(
    req: RefreshTokenRequestDTO,
    auth_service: AuthService = Depends(get_auth_service_imp)
):
    return await auth_service.refresh_access_token(req.refresh_token)