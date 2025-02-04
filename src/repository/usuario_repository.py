from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, func, or_, Text, cast, update
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.usuario import Usuario
from src.model.entity.trabajador import Trabajador
from src.model.entity.rol import Rol

class UsuarioRepository:

    @staticmethod
    def add_usuario(usuario: Usuario) -> Usuario:
        with Session(engine) as session:
            try:
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            except SQLAlchemyError as e:
                raise DatabaseException("Error al guardar el usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al guardar el usuario en la base de datos") from e


    @staticmethod
    def get_usuarios_pagination(page: int = 1, page_size: int = 10, is_active: bool = True) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                result = session.exec(
                    select(Usuario.id, Usuario.nombre_usuario, Usuario.fecha_creacion, Usuario.fecha_actualizacion,
                           Usuario.is_active,
                           Rol.nombre_rol.label("rol_nombre"), Trabajador.nombres.label("trabajador_nombre"))
                    .join(Rol, Usuario.rol_id == Rol.id)
                    .join(Trabajador, Usuario.trabajador_id == Trabajador.id)
                    .where(Usuario.is_active == is_active)
                    .order_by(Usuario.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()

                usuarios_data = [dict(row._mapping) for row in result]
                total_items = session.exec(
                    select(func.count()).select_from(Usuario).where(Usuario.is_active == is_active)).first()
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
                raise DatabaseException("Error al obtener la lista de usuarios") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener la lista de usuarios") from e


    @staticmethod
    def update_user(usuario: Usuario) -> Usuario:
        with Session(engine) as session:
            try:
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            except SQLAlchemyError as e:
                raise DatabaseException("Error al actualizar el usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al actualizar el usuario en la base de datos") from e


    @staticmethod
    def delete_by_id(usuario_id: int) -> None:
        with Session(engine) as session:
            try:
                usuario = session.exec(select(Usuario).where(Usuario.id == usuario_id)).first()
                session.delete(usuario)
                session.commit()
            except SQLAlchemyError as e:
                raise DatabaseException("Error al eliminar el usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al eliminar el usuario en la base de datos") from e


    @staticmethod
    def update_status_user_by_id(usuario_id: int, active: bool) -> None:
        with Session(engine) as session:
            try:
                session.exec(
                    update(Usuario)
                    .where(Usuario.id == usuario_id)
                    .values(is_active=active)
                )
                session.commit()
            except SQLAlchemyError as e:
                raise DatabaseException("Error al actualizar el estado del usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al actualizar el estado del usuario en la base de datos") from e


    @staticmethod
    def get_by_id(usuario_id: int) -> Optional[Usuario]:
        with Session(engine) as session:
            try:
                usuario = session.exec(select(Usuario).where(Usuario.id == usuario_id)).first()
                return usuario
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el usuario de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el usuario de la base de datos") from e


    @staticmethod
    def exists_by_username(username: str) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Usuario).where(Usuario.nombre_usuario == username)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del usuario en la base de datos") from e


    @staticmethod
    def exists_by_trabajador_id(trabajador_id: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Usuario).where(Usuario.trabajador_id == trabajador_id)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del usuario en la base de datos") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Dict[str, Any]]:
        with Session(engine) as session:
            try:
                search_filter = or_(
                    cast(Usuario.nombre_usuario, Text).contains(search_string),
                    Usuario.nombre_usuario.contains(search_string),
                    Trabajador.nombres.contains(search_string),
                    Rol.nombre_rol.contains(search_string)
                )
                result = session.exec(
                    select(Usuario.id, Usuario.nombre_usuario, Usuario.fecha_creacion, Usuario.fecha_actualizacion,
                           Usuario.is_active,
                           Rol.nombre_rol, Trabajador.nombres)
                    .join(Rol, Usuario.rol_id == Rol.id)
                    .join(Trabajador, Usuario.trabajador_id == Trabajador.id)
                    .where(search_filter)
                ).all()

                usuarios_data = [dict(row._mapping) for row in result]

                return usuarios_data
            except SQLAlchemyError as e:
                raise DatabaseException("Error al buscar el usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al buscar el usuario en la base de datos") from e


    @staticmethod
    def exists_by_id(usuario_id: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Usuario).where(Usuario.id == usuario_id)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del usuario en la base de datos") from e


    @staticmethod
    def update_password_by_id(usuario_id: int, new_password: str) ->bool:
        with Session(engine) as session:
            try:
                session.exec(
                    update(Usuario)
                    .where(Usuario.id == usuario_id)
                    .values(contrasena=new_password)
                )
                session.commit()
                return True
            except SQLAlchemyError as e:
                raise DatabaseException("Error al actualizar la contraseña del usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al actualizar la contraseña del usuario en la base de datos") from e


    @staticmethod
    def find_user_by_username(username: str) -> Optional[Usuario]:
        with Session(engine) as session:
            try:
                usuario = session.exec(
                    select(Usuario, Trabajador, Rol)
                    .join(Rol, Usuario.rol_id == Rol.id)
                    .join(Trabajador, Usuario.trabajador_id == Trabajador.id)
                    .where(Usuario.nombre_usuario == username)
                ).first()
                return usuario
            except SQLAlchemyError as e:
                raise DatabaseException("Error al buscar el usuario en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al buscar el usuario en la base de datos") from e







