from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.service.auth_service import AuthService
from src.repository.usuario_repository import UsuarioRepository
from src.model.entity.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: AuthService = Depends(),
    usuario_repo: UsuarioRepository = Depends()
) -> Usuario:
    username = auth_service.get_username_from_token(token)
    user_data = usuario_repo.find_user_by_username(username)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró el usuario asociado al token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user, trabajador, rol = user_data
    return user, trabajador, rol
