from typing import Dict, Any, List
from sqlmodel import Session, text, select, func
from src.db.database import engine
from src.model.entity.recepcion_documento import RecepcionDocumento

class RecepcionDocumentoRepository:

    @staticmethod
    def add_received_document(recepcion_documento: RecepcionDocumento) -> RecepcionDocumento:
        with Session(engine) as session:
            session.add(recepcion_documento)
            session.commit()
            session.refresh(recepcion_documento)
        return recepcion_documento


    @staticmethod
    def update_received_document(recepcion_documento: RecepcionDocumento) -> RecepcionDocumento:
        with Session(engine) as session:
            session.add(recepcion_documento)
            session.commit()
            session.refresh(recepcion_documento)
        return recepcion_documento


    @staticmethod
    def delete_received_document_by_id(recepcion_documento_id: int) -> None:
        with Session(engine) as session:
            recepcion_documento = session.get(RecepcionDocumento, recepcion_documento_id)
            if recepcion_documento:
                session.delete(recepcion_documento)
                session.commit()


    @staticmethod
    def exists_by_id(recepcion_documento_id: int) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(RecepcionDocumento).where(RecepcionDocumento.id == recepcion_documento_id)).first() is not None
        return exists


    @staticmethod
    def get_all_paginated(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            recepcion_documentos = session.exec(
                select(RecepcionDocumento)
                .order_by(RecepcionDocumento.id)
                .offset(offset)
                .limit(page_size)
            ).all()
            total_items = session.exec(select(func.count()).select_from(RecepcionDocumento)).first()
            total_pages = (total_items + page_size - 1) // page_size

        return {
            "data": recepcion_documentos,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }