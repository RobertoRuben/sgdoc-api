from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from src.dto.auth_request import AuthRequest
from src.dto.auth_response import AuthResponse
from src.dto.refresh_token import RefreshTokenRequest
from src.dto.user_info_response import UserInfoResponse
from src.service.auth_service import AuthService
from src.repository.usuario_repository import UsuarioRepository
from src.model.entity.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: AuthService = Depends(),
    usuario_repo: UsuarioRepository = Depends()
) -> Usuario:
    username = auth_service.get_username_from_token(token)
    user = usuario_repo.find_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró el usuario asociado al token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

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
def read_users_me(
    current_user: Annotated[Usuario, Depends(get_current_user)]
):
    return UserInfoResponse(
        id=current_user.id,
        username=current_user.nombre_usuario,
        rol_id=current_user.rol_id,
        is_active=current_user.is_active
    )


@router.post("/refresh", response_model=AuthResponse)
def refresh_token(
    req: RefreshTokenRequest,
    auth_service: AuthService = Depends()
):
    return auth_service.refresh_access_token(req.refresh_token)

