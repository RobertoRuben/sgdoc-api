from typing import List, Tuple
from sqlmodel import Session, select, func
from sqlalchemy.exc import SQLAlchemyError
from src.db.database import engine
from src.exception import DatabaseException
from src.model.entity.documento import Documento
from src.model.entity.derivacion import Derivacion
from src.model.entity.caserio import Caserio

class MesaPartesDashboardRepository:

    @staticmethod
    def get_number_documentos_by_current_date() -> int:
        with Session(engine) as session:
            try:
                query = select(func.count(Documento.id)).where(
                    func.date(Documento.fecha_ingreso) == func.current_date())
                result = session.exec(query).first() or 0
                return result
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el número de documentos en la fecha actual") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el número de documentos en la fecha actual") from e


    @staticmethod
    def get_number_documentos_derivados_current_date() -> int:
        with Session(engine) as session:
            try:
                query = select(func.count(Documento.id)).join(
                    Derivacion
                ).where(
                    func.date(Derivacion.fecha) == func.current_date()
                )
                result = session.exec(query).first() or 0
                return result
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el número de documentos derivados en la fecha actual") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el número de documentos derivados en la fecha actual") from e


    @staticmethod
    def get_number_documentos_pendientes_derivar_current_date() -> int:
        with Session(engine) as session:
            try:
                documentos_derivados = select(Documento.id).join(Derivacion).distinct()

                query = select(func.count(Documento.id)).where(
                    func.date(Documento.fecha_ingreso) == func.current_date(),
                    Documento.id.not_in(documentos_derivados)
                )

                result = session.exec(query).first() or 0
                return result
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el número de documentos pendientes de derivar en la fecha actual") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el número de documentos pendientes de derivar en la fecha actual") from e


    @staticmethod
    def get_caserios_with_documentos_count_current_date() -> List[Tuple[str, int]]:
        with Session(engine) as session:
            try:
                query = select(
                    Caserio.nombre_caserio,
                    func.count(Documento.id).label('total_documentos')
                ).outerjoin(
                    Documento, (Caserio.id == Documento.caserio_id) &
                    (func.date(Documento.fecha_ingreso) == func.current_date())
                ).group_by(
                    Caserio.id,
                    Caserio.nombre_caserio
                ).order_by(
                    func.count(Documento.id).desc(),
                    Caserio.nombre_caserio
                ).limit(5)
                result = session.exec(query).all()
                return list(result)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los caseríos con más documentos en la fecha actual") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los caseríos con más documentos en la fecha actual") from e