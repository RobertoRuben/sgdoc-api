from sqlmodel import Session, select, func
from typing import List, Tuple
from src.db.database import engine
from src.model.entity.documento import Documento
from src.model.entity.derivacion import Derivacion
from src.model.entity.caserio import Caserio

class DocumentosByCurrentDateRepository:

    @staticmethod
    def get_number_documentos_by_current_date() -> int:
        with Session(engine) as session:
            query = select(func.count(Documento.id)).where(
                func.date(Documento.fecha_ingreso) == func.current_date())
            result = session.exec(query).first() or 0
            return result


    @staticmethod
    def get_number_documentos_derivados_current_date() -> int:
        with Session(engine) as session:
            query = select(func.count(Documento.id)).join(
                Derivacion
            ).where(
                func.date(Derivacion.fecha) == func.current_date()
            )
            result = session.exec(query).first() or 0
            return result


    @staticmethod
    def get_number_documentos_pendientes_derivar_current_date() -> int:
        with Session(engine) as session:
            documentos_derivados = select(Documento.id).join(
                Derivacion
            ).distinct()

            query = select(func.count(Documento.id)).where(
                func.date(Documento.fecha_ingreso) == func.current_date(),
                Documento.id.not_in(documentos_derivados)
            )

            result = session.exec(query).first() or 0
            return result


    @staticmethod
    def get_caserios_with_documentos_count_current_date() -> List[Tuple[str, int]]:
        with Session(engine) as session:
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
            result = session.exec(query).all()
            return result