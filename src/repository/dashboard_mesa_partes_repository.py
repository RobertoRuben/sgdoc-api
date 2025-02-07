from typing import List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Documento, Derivacion, Caserio


class DashboardMesaPartesRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_number_documentos_by_current_date(self) -> int:
        try:
            query = select(func.count(Documento.id)).where(
                func.date(Documento.fecha_ingreso) == func.current_date()
            )
            result = await self.session.exec(query)
            count = result.first() or 0
            return count
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el número de documentos en la fecha actual",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener el número de documentos en la fecha actual",
                error_details=str(e)
            ) from e


    async def get_number_documentos_derivados_current_date(self) -> int:
        try:
            query = select(func.count(Documento.id)).join(Derivacion).where(
                func.date(Derivacion.fecha) == func.current_date()
            )
            result = await self.session.exec(query)
            count = result.first() or 0
            return count
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el número de documentos derivados en la fecha actual",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener el número de documentos derivados en la fecha actual",
                error_details=str(e)
            ) from e


    async def get_number_documentos_pendientes_derivar_current_date(self) -> int:
        try:
            # Selecciona los IDs de los documentos que ya tienen derivación
            documentos_derivados = select(Documento.id).join(Derivacion).distinct()
            query = select(func.count(Documento.id)).where(
                func.date(Documento.fecha_ingreso) == func.current_date(),
                Documento.id.not_in(documentos_derivados)
            )
            result = await self.session.exec(query)
            count = result.first() or 0
            return count
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el número de documentos pendientes de derivar en la fecha actual",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener el número de documentos pendientes de derivar en la fecha actual",
                error_details=str(e)
            ) from e


    async def get_caserios_with_documentos_count_current_date(self) -> List[Tuple[str, int]]:
        try:
            query = select(
                Caserio.nombre_caserio,
                func.count(Documento.id).label('total_documentos')
            ).outerjoin(
                Documento,
                (Caserio.id == Documento.caserio_id) &
                (func.date(Documento.fecha_ingreso) == func.current_date())
            ).group_by(
                Caserio.id,
                Caserio.nombre_caserio
            ).order_by(
                func.count(Documento.id).desc(),
                Caserio.nombre_caserio
            ).limit(5)
            result = await self.session.exec(query)
            rows = result.all()
            return list(rows)
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener los caseríos con más documentos en la fecha actual",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener los caseríos con más documentos en la fecha actual",
                error_details=str(e)
            ) from e
