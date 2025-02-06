from fastapi import Depends
from src.exception import UnauthorizedException, ForbiddenException
from src.dto.auth_request_dto import AuthRequestDTO
from src.dto.auth_response_dto import AuthResponseDTO
from src.security.argon2_hasher import Argon2PasswordHasher
from src.security.token_manager import TokenManager
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

    def authenticate_user(self, auth_request: AuthRequestDTO) -> AuthResponseDTO:
        user_data = self.usuario_repository.find_user_by_username(auth_request.username)
        if not user_data:
            raise UnauthorizedException(
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"}
            )

        user, trabajador, rol = user_data

        if not user.is_active:
            raise ForbiddenException(
                detail="Este usuario está inactivo. Contacte al administrador."
            )

        if not self.argon2_hasher.verify_password(user.contrasena, auth_request.password):
            raise UnauthorizedException(
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"}
            )

        access_token = self.token_manager.create_access_token(
            {"sub": user.nombre_usuario, "scope": "access"}
        )
        refresh_token = self.token_manager.create_refresh_token(
            {"sub": user.nombre_usuario, "scope": "refresh"}
        )

        return AuthResponseDTO(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            user_id=user.id,
            rol_name=rol.nombre_rol,
            area_id=trabajador.area_id
        )


    def get_username_from_token(self, token: str) -> str:
        payload = self.token_manager.decode_token(token)
        username: str = payload.get("sub")
        if not username:
            raise UnauthorizedException(
                detail="Token inválido: faltó 'sub'",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return username


    def refresh_access_token(self, refresh_token: str) -> AuthResponseDTO:
        payload = self.token_manager.decode_token(refresh_token)
        username: str = payload.get("sub")
        scope: str = payload.get("scope")

        if not username or scope != "refresh":
            raise UnauthorizedException(detail="Refresh token inválido")

        user_data = self.usuario_repository.find_user_by_username(username)
        if not user_data:
            raise UnauthorizedException(detail="Usuario no encontrado")

        user, trabajador, rol = user_data

        if not user.is_active:
            raise ForbiddenException(
                detail="Este usuario está inactivo. Contacte al administrador."
            )

        new_access_token = self.token_manager.create_access_token(
            {"sub": user.nombre_usuario, "scope": "access"}
        )

        return AuthResponseDTO(
            access_token=new_access_token,
            token_type="bearer"
        )
