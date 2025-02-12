from typing import List, Any, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session

class DashboardRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_total_documents_by_documentary_scope(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None
    ) -> List[Dict[str, Any]]:
        try:
            query = text(
                """
                SELECT fn_documentos_ingresos_por_ambito(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )

            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            total_documents_by_documentary_scope = result.scalar()

            return total_documents_by_documentary_scope if total_documents_by_documentary_scope else []
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener los ingresos por ámbito",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener los ingresos por ámbito",
                error_details=str(e)
            ) from e


    async def get_total_documents_by_village(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None
    ) -> List[Dict[str, Any]]:
        try:
            query = text(
                """
                SELECT fn_documentos_ingresos_por_caserio(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )
            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            total_documents_by_village = result.scalar()

            return total_documents_by_village if total_documents_by_village else []
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener los ingresos por caserío",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener los ingresos por caserío",
                error_details=str(e)
            ) from e


    async def get_total_documents_by_centro_poblado(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None
    ) -> List[Dict[str, Any]]:
        try:
            query = text(
                """
                SELECT fn_documentos_ingresos_por_centros_poblados(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )
            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            total_documents_by_centro_poblado = result.scalar()

            return total_documents_by_centro_poblado if total_documents_by_centro_poblado else []
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener los ingresos por centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener los ingresos por centro poblado",
                error_details=str(e)
            ) from e


    async def get_average_total_documents(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None
    ) -> Dict[str, Any]:
        try:
            query = text(
                """
                SELECT fn_documentos_promedio_ingresos(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )
            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            average_total_documents = result.scalar()

            return average_total_documents if average_total_documents else {}
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener el promedio de documentos ingresados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener el promedio de documentos ingresados",
                error_details=str(e)
            ) from e


    async def get_top_villages_with_most_documents(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None

    ) -> Dict[str, Any]:
        try:
            query = text(
                """
                SELECT fn_documentos_top_5_caserios_mas_ingresos(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )
            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            top_village_by_documents = result.scalar()

            return top_village_by_documents if top_village_by_documents else {}
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener el promedio de documentos ingresados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener el promedio de documentos ingresados",
                error_details=str(e)
            ) from e


    async def get_top_villages_with_least_documents(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None

    ) -> Dict[str, Any]:
        try:
            query = text(
                """
                SELECT fn_documentos_top_5_caserios_menos_ingresos(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )
            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            top_village_by_documents = result.scalar()

            return top_village_by_documents if top_village_by_documents else {}
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener el promedio de documentos ingresados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener el promedio de documentos ingresados",
                error_details=str(e)
            ) from e


    async def get_total_documents(
            self,
            p_start_year: int | None = None,
            p_end_year: int | None = None,
            p_start_month: int | None = None,
            p_end_month: int | None = None
    ) -> Dict[str, Any]:
        try:
            query = text(
                """
                SELECT fn_documentos_total_ingresos(
                    :p_start_year,
                    :p_end_year,
                    :p_start_month,
                    :p_end_month
                )
                """
            )
            result = await self.session.execute(query, {
                "p_start_year": p_start_year,
                "p_end_year": p_end_year,
                "p_start_month": p_start_month,
                "p_end_month": p_end_month
            })

            total_documents = result.scalar()

            return total_documents if total_documents else {}
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener el total de documentos ingresados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener el total de documentos ingresados",
                error_details=str(e)
            ) from e

