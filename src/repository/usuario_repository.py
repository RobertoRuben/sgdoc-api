from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_, Text, cast, update
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Usuario, Rol, Trabajador

class UsuarioRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_usuario(self, usuario: Usuario) -> Usuario:
        try:
            self.session.add(usuario)
            await self.session.commit()
            await self.session.refresh(usuario)
            return usuario
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al guardar el usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al guardar el usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def get_usuarios_pagination(self, page: int = 1, page_size: int = 10, is_active: bool = True) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(
                    Usuario.id,
                    Usuario.nombre_usuario,
                    Usuario.fecha_creacion,
                    Usuario.fecha_actualizacion,
                    Usuario.is_active,
                    Rol.nombre_rol.label("rol_nombre"),
                    Trabajador.nombres.label("trabajador_nombre")
                )
                .join(Rol, Usuario.rol_id == Rol.id)
                .join(Trabajador, Usuario.trabajador_id == Trabajador.id)
                .where(Usuario.is_active == is_active)
                .order_by(Usuario.id)
                .offset(offset)
                .limit(page_size)
            )
            rows = result.all()
            usuarios_data = [dict(row._mapping) for row in rows]
            total_result = await self.session.exec(
                select(func.count()).select_from(Usuario).where(Usuario.is_active == is_active)
            )
            total_items = total_result.first() or 0
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": usuarios_data,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener la lista de usuarios",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener la lista de usuarios",
                error_details=str(e)
            ) from e


    async def update_user(self, usuario: Usuario) -> Usuario:
        try:
            self.session.add(usuario)
            await self.session.commit()
            await self.session.refresh(usuario)
            return usuario
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar el usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido al actualizar el usuario en la base de datos",
                error_details=str(e)
            )from e


    async def delete_by_id(self, usuario_id: int) -> None:
        try:
            result = await self.session.exec(select(Usuario).where(Usuario.id == usuario_id))
            usuario = result.first()
            await self.session.delete(usuario)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al eliminar el usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido al eliminar el usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def update_status_user_by_id(self, usuario_id: int, active: bool) -> None:
        try:
            await self.session.exec(
                update(Usuario)
                .where(Usuario.id == usuario_id)
                .values(is_active=active)
            )
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar el estado del usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido al actualizar el estado del usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        try:
            result = await self.session.exec(select(Usuario).where(Usuario.id == usuario_id))
            usuario = result.first()
            return usuario
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el usuario de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener el usuario de la base de datos",
                error_details=str(e)
            ) from e


    async def exists_by_username(self, username: str) -> bool:
        try:
            result = await self.session.exec(select(Usuario).where(Usuario.nombre_usuario == username))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al verificar la existencia del usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al verificar la existencia del usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def exists_by_trabajador_id(self, trabajador_id: int) -> bool:
        try:
            result = await self.session.exec(select(Usuario).where(Usuario.trabajador_id == trabajador_id))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al verificar la existencia del usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al verificar la existencia del usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Dict[str, Any]]:
        try:
            search_filter = or_(
                cast(Usuario.nombre_usuario, Text).contains(search_string),
                Usuario.nombre_usuario.contains(search_string),
                Trabajador.nombres.contains(search_string),
                Rol.nombre_rol.contains(search_string)
            )
            result = await self.session.exec(
                select(
                    Usuario.id,
                    Usuario.nombre_usuario,
                    Usuario.fecha_creacion,
                    Usuario.fecha_actualizacion,
                    Usuario.is_active,
                    Rol.nombre_rol,
                    Trabajador.nombres
                )
                .join(Rol, Usuario.rol_id == Rol.id)
                .join(Trabajador, Usuario.trabajador_id == Trabajador.id)
                .where(search_filter)
            )
            rows = result.all()
            usuarios_data = [dict(row._mapping) for row in rows]
            return usuarios_data
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al buscar el usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al buscar el usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def exists_by_id(self, usuario_id: int) -> bool:
        try:
            result = await self.session.exec(select(Usuario).where(Usuario.id == usuario_id))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al verificar la existencia del usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al verificar la existencia del usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def update_password_by_id(self, usuario_id: int, new_password: str) -> bool:
        try:
            await self.session.exec(
                update(Usuario)
                .where(Usuario.id == usuario_id)
                .values(contrasena=new_password)
            )
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar la contraseña del usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido al actualizar la contraseña del usuario en la base de datos",
                error_details=str(e)
            ) from e


    async def find_user_by_username(self, username: str) -> Optional[Usuario]:
        try:
            result = await self.session.exec(
                select(Usuario, Trabajador, Rol)
                .join(Rol, Usuario.rol_id == Rol.id)
                .join(Trabajador, Usuario.trabajador_id == Trabajador.id)
                .where(Usuario.nombre_usuario == username)
            )
            return result.first()
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al buscar el usuario en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al buscar el usuario en la base de datos",
                error_details=str(e)
            ) from e
