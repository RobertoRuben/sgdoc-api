from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.security.dependencies import get_current_user
from typing import Annotated

from src.dto.auth_request import AuthRequest
from src.dto.auth_response import AuthResponse
from src.dto.refresh_token import RefreshTokenRequest
from src.dto.user_info_response import UserInfoResponse
from src.service.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=AuthResponse)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends()
) -> AuthResponse:
    auth_request = AuthRequest(
        username=form_data.username,
        password=form_data.password
    )
    return auth_service.authenticate_user(auth_request)


@router.get("/me", response_model=UserInfoResponse)
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


@router.post("/refresh", response_model=AuthResponse)
def refresh_token(
    req: RefreshTokenRequest,
    auth_service: AuthService = Depends()
):
    return auth_service.refresh_access_token(req.refresh_token)

