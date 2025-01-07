from typing import List, Optional
from sqlmodel import  Session, select, func, or_
from src.db.database import engine
from src.model.entity.detalle_derivacion import DetalleDerivacion

class DetalleDerivacionRepository:

    @staticmethod
    def add_detalle_derivacion(detalle_derivacion: DetalleDerivacion) -> DetalleDerivacion:
        with Session(engine) as session:
            session.add(detalle_derivacion)
            session.commit()
            session.refresh(detalle_derivacion)
        return detalle_derivacion


    @staticmethod
    def get_all_by_derivacion_id(derivacion_id: int) -> List[DetalleDerivacion]:
        with Session(engine) as session:
            detalles_derivacion = session.exec(select(DetalleDerivacion).where(DetalleDerivacion.derivacion_id == derivacion_id)).all()
        return detalles_derivacion


    @staticmethod
    def update_detalle_derivacion(detalle_derivacion: DetalleDerivacion) -> DetalleDerivacion:
        with Session(engine) as session:
            session.add(detalle_derivacion)
            session.commit()
            session.refresh(detalle_derivacion)
        return detalle_derivacion


    @staticmethod
    def delete_by_id(detalle_derivacion_id: int) -> None:
        with Session(engine) as session:
            detalle_derivacion = session.get(DetalleDerivacion, detalle_derivacion_id)
            if detalle_derivacion:
                session.delete(detalle_derivacion)
                session.commit()


    @staticmethod
    def exists_detalle_derivacion_by_id(detalle_derivacion_id: int) -> bool:
        with Session(engine) as session:
            return session.exec(select(func.count(DetalleDerivacion.id)).where(DetalleDerivacion.id == detalle_derivacion_id)).scalar() > 0

    @staticmethod
    def get_by_id(detalle_derivacion_id: int) -> Optional[DetalleDerivacion]:
        with Session(engine) as session:
            detalle_derivacion = session.get(DetalleDerivacion, detalle_derivacion_id)
        return detalle_derivacion
