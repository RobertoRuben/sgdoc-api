from fastapi import HTTPException, status, Depends
from typing import Optional
from src.dto.auth_request import AuthRequest
from src.dto.auth_response import AuthResponse
from src.security.argon2_hasher import Argon2PasswordHasher
from src.security.token_manager import TokenManager
from src.model.entity.usuario import Usuario
from src.repository.usuario_repository import UsuarioRepository

class AuthService:
    def __init__(
            self,
            argon2_hasher: Argon2PasswordHasher = Depends(),
            usuario_repository: UsuarioRepository = Depends(),
            token_manager: TokenManager = Depends()
    ):
        self.argon2_hasher = argon2_hasher
        self.usuario_repository = usuario_repository
        self.token_manager = token_manager

    def authenticate_user(self, auth_request: AuthRequest) -> AuthResponse:
        user: Optional[Usuario] = self.usuario_repository.find_user_by_username(auth_request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este usuario está inactivo. Contacte al administrador.",
            )
        if not self.argon2_hasher.verify_password(user.contrasena, auth_request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.token_manager.create_access_token(
            {"sub": user.nombre_usuario, "scope": "access"}
        )
        refresh_token = self.token_manager.create_refresh_token(
            {"sub": user.nombre_usuario, "scope": "refresh"}
        )

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token
        )


    def get_username_from_token(self, token: str) -> str:
        payload = self.token_manager.decode_token(token)
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: faltó 'sub'",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username


    def refresh_access_token(self, refresh_token: str) -> AuthResponse:
        payload = self.token_manager.decode_token(refresh_token)
        username: str = payload.get("sub")
        scope: str = payload.get("scope")

        if not username or scope != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido",
            )

        user = self.usuario_repository.find_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se encontró usuario para este refresh token",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo. No se puede refrescar.",
            )

        new_access_token = self.token_manager.create_access_token(
            {"sub": user.nombre_usuario, "scope": "access"}
        )

        return AuthResponse(
            access_token=new_access_token,
            token_type="bearer"
        )
