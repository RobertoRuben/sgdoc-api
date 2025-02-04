from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, func, or_
from sqlalchemy.exc import SQLAlchemyError
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.categoria import Categoria

class CategoriaRepository:

    @staticmethod
    def add_categoria(categoria: Categoria) -> Categoria:
        with Session(engine) as session:
            try:
                session.add(categoria)
                session.commit()
                session.refresh(categoria)
                return categoria
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al agregar la categoría") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al agregar la categoría") from e


    @staticmethod
    def get_all_categorias() -> List[Categoria]:
        with Session(engine) as session:
            try:
                categorias = session.exec(select(Categoria)).all()
                return list(categorias)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener las categorías") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener las categorías") from e


    @staticmethod
    def update_categoria(categoria: Categoria) -> Categoria:
        with Session(engine) as session:
            try:
                session.add(categoria)
                session.commit()
                session.refresh(categoria)
                return categoria
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar la categoría") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al actualizar la categoría") from e


    @staticmethod
    def delete_by_id(categoria_id: int) -> None:
        with Session(engine) as session:
            try:
                categoria = session.get(Categoria, categoria_id)
                if categoria:
                    session.delete(categoria)
                    session.commit()
            except SQLAlchemyError as e:
                raise DatabaseException("Error al eliminar la categoría") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al eliminar la categoría") from e


    @staticmethod
    def get_by_id(categoria_id: int) -> Optional[Categoria]:
        with Session(engine) as session:
            try:
                categoria = session.get(Categoria, categoria_id)
                return categoria
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener la categoría") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener la categoría") from e


    @staticmethod
    def exists(nombre_categoria: str) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(
                    select(Categoria).where(Categoria.nombre_categoria == nombre_categoria)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia de la categoría") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia de la categoría") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Categoria]:
        with Session(engine) as session:
            try:
                search_filter = or_(
                    Categoria.nombre_categoria.contains(search_string)
                )
                categorias = session.exec(select(Categoria).where(search_filter)).all()
                return list(categorias)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al buscar la categoría") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al buscar la categoría") from e


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                categorias = session.exec(
                    select(Categoria)
                    .order_by(Categoria.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()
                total_items = session.exec(select(func.count()).select_from(Categoria)).first()
                total_pages = (total_items + page_size - 1) // page_size

                return {
                    "data": categorias,
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": total_items,
                        "total_pages": total_pages
                    }
                }

            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener las categorías paginadas") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener las categorías paginadas") from e