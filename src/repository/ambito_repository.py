from typing import List, Dict, Any, Optional
from fastapi import Depends
from sqlmodel import select, or_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exception import DatabaseException
from src.db.database import get_session
from src.model.entity.ambito import Ambito

class AmbitoRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def add_ambito(self, ambito: Ambito) -> Ambito:
        try:
            self.session.add(ambito)
            await self.session.commit()
            await self.session.refresh(ambito)
            return ambito
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al agregar el ambito",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al agregar el ambito",
                error_details=str(e)
            ) from e


    async def get_all_ambitos(self) -> List[Ambito]:
        try:
            result = await self.session.exec(select(Ambito))
            ambitos = result.all()
            return list(ambitos)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener la lista de ambitos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener la lista de ambitos",
                error_details=str(e)
            ) from e


    async def update_ambito(self, ambito: Ambito) -> Ambito:
        try:
            self.session.add(ambito)
            await self.session.commit()
            await self.session.refresh(ambito)
            return ambito
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al actualizar el ambito",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al actualizar el ambito",
                error_details=str(e)
            ) from e


    async def delete_ambito_by_id(self, ambito_id: int) -> bool:
        try:
            ambito = await self.session.get(Ambito, ambito_id)
            if ambito:
                await self.session.delete(ambito)
                await self.session.commit()

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al eliminar el ambito",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al eliminar el ambito",
                error_details=str(e)
            ) from e


    async def get_ambito_by_id(self, ambito_id: int) -> Optional[Ambito]:
        try:
            ambito = await self.session.get(Ambito, ambito_id)
            return ambito

        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener el ambito",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener el ambito",
                error_details=str(e)
            ) from e


    async def exists(self, nombre_ambito: str) -> bool:
        try:
            result =  await self.session.exec(
                select(Ambito).where(Ambito.nombre_ambito == nombre_ambito)
            )
            exists = result.first() is not None
            return exists

        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al verificar la existencia del ambito",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al verificar la existencia del ambito",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) ->List[Ambito]:
        try:
            search_filter = or_(Ambito.nombre_ambito.contains(search_string))
            result = await self.session.exec(select(Ambito).where(search_filter))
            ambitos = result.all()
            return list(ambitos)

        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al buscar el ambito",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al buscar el ambito",
                error_details=str(e)
            ) from e


    async def get_all_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            offset = (page - 1) * page_size

            result = await self.session.exec(
                select(Ambito)
                .order_by(Ambito.id)
                .offset(offset)
                .limit(page_size)
            )
            ambitos = result.all()

            result_count = await self.session.exec(select(func.count()).select_from(Ambito))
            total_items = result_count.first()
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": ambitos,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio al obtener la lista de ambitos paginados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener la lista de ambitos paginados",
                error_details=str(e)
            ) from e





