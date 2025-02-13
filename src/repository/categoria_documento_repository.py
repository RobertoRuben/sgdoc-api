from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Categoria

class CategoriaDocumentoRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_categoria(self, categoria: Categoria) -> Categoria:
        try:
            self.session.add(categoria)
            await self.session.commit()
            await self.session.refresh(categoria)
            return categoria
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al agregar la categoría",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al agregar la categoría",
                error_details=str(e)
            ) from e


    async def get_all_categorias(self) -> List[Categoria]:
        try:
            result = await self.session.exec(select(Categoria))
            categorias = result.all()
            return list(categorias)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener las categorías",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener las categorías",
                error_details=str(e)
            ) from e


    async def update_categoria(self, categoria: Categoria) -> Categoria:
        try:
            self.session.add(categoria)
            await self.session.commit()
            await self.session.refresh(categoria)
            return categoria
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al actualizar la categoría",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al actualizar la categoría",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, categoria_id: int) -> None:
        try:
            categoria = await self.session.get(Categoria, categoria_id)
            if categoria:
                await self.session.delete(categoria)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al eliminar la categoría",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al eliminar la categoría",
                error_details=str(e)
            ) from e


    async def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        try:
            categoria = await self.session.get(Categoria, categoria_id)
            return categoria
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener la categoría",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener la categoría",
                error_details=str(e)
            ) from e


    async def exists(self, nombre_categoria: str) -> bool:
        try:
            result = await self.session.exec(
                select(Categoria).where(Categoria.nombre_categoria == nombre_categoria)
            )
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al verificar la existencia de la categoría",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al verificar la existencia de la categoría",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Categoria]:
        try:
            search_filter = or_(Categoria.nombre_categoria.contains(search_string))
            result = await self.session.exec(
                select(Categoria).where(search_filter)
            )
            categorias = result.all()
            return list(categorias)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al buscar la categoría",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al buscar la categoría",
                error_details=str(e)
            ) from e


    async def get_all_pagination(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(Categoria)
                .order_by(Categoria.id)
                .offset(offset)
                .limit(page_size)
            )
            categorias = result.all()
            count_result = await self.session.exec(
                select(func.count()).select_from(Categoria)
            )
            total_items = count_result.first()
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
            raise DatabaseException(
                detail="Error al obtener las categorías paginadas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener las categorías paginadas",
                error_details=str(e)
            ) from e
