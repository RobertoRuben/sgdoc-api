from typing import List, Optional, Dict, Any, Tuple
from sqlmodel import Session, select, func, or_, Text, text
from datetime import date
from src.db.database import engine
from src.model.entity.documento import Documento


class DocumentoRepository:

    @staticmethod
    def add_documentos(documento: Documento) -> Documento:
        with Session(engine) as session:
            session.add(documento)
            session.commit()
            session.refresh(documento)
        return documento


    @staticmethod
    def update_document(documento: Documento) -> Documento:
        with Session(engine) as session:
            session.add(documento)
            session.commit()
            session.refresh(documento)
        return documento


    @staticmethod
    def get_document_by_id(documento_id: int) -> Documento:
        with Session(engine) as session:
            documento = session.exec(select(Documento).where(Documento.id == documento_id)).first()
        return documento


    @staticmethod
    def delete_document_by_id(documento_id: int):
        with Session(engine) as session:
            documento = session.get(Documento, documento_id)
            if documento:
                session.delete(documento)
                session.commit()


    @staticmethod
    def exists_by_id(documento_id: int) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Documento).where(Documento.id == documento_id)).first() is not None
        return exists


    @staticmethod
    def exists_by_name(documento_name: str) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Documento).where(Documento.nombre == documento_name)).first() is not None
        return exists


    @staticmethod
    def get_document_bytes_and_name_by_id(documento_id: int) -> Tuple[Optional[bytes], Optional[str]]:
        with Session(engine) as session:
            result = session.exec(
                select(Documento.documento_bytes, Documento.nombre)
                .where(Documento.id == documento_id)
            ).first()
        if result:
            documento_bytes, nombre = result
            return documento_bytes, nombre
        return None, None


    @staticmethod
    def get_documents_by_current_date(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""SELECT fn_documentos_get_by_current_date_paginated(:page, :page_size)""")
            connection = session.connection()
            result = connection.execute(query, {"page": page, "page_size": page_size}).scalar()

            if result:
                return result

            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }


    @staticmethod
    def get_all_documents_paginated(p_page: int, p_page_size: int) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""SELECT fn_get_documentos_paginated(:p_page, :p_page_size)""")
            connection = session.connection()
            result = connection.execute(query, {"p_page": p_page, "p_page_size": p_page_size}).scalar()

            if result:
                return result

            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": p_page,
                        "page_size": p_page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }


    @staticmethod
    def get_sent_documents_by_area_id(
        p_area_origen_id: int,
        p_search_document: int = None,
        p_id_caserio: int = None,
        p_id_centro_poblado: int = None,
        p_id_ambito: int = None,
        p_nombre_categoria: str = None,
        p_fecha_ingreso: str = None,
        p_page: int = 1,
        p_page_size: int = 10
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""
                SELECT public.fn_documentos_get_documentos_enviados_by_area_id(
                    :p_area_origen_id,
                    :p_search_document,
                    :p_id_caserio,
                    :p_id_centro_poblado,
                    :p_id_ambito,
                    :p_nombre_categoria,
                    :p_fecha_ingreso,
                    :p_page,
                    :p_page_size
                )
            """)
            connection = session.connection()
            result = connection.execute(query, {
                "p_area_origen_id": p_area_origen_id,
                "p_search_document": p_search_document,
                "p_id_caserio": p_id_caserio,
                "p_id_centro_poblado": p_id_centro_poblado,
                "p_id_ambito": p_id_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso,
                "p_page": p_page,
                "p_page_size": p_page_size
            }).scalar()

            if result:
                return result
            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": p_page,
                        "page_size": p_page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }


    @staticmethod
    def get_received_documents_by_area_id(
        p_area_destino_id: int,
        p_search_document: int = None,
        p_id_caserio: int = None,
        p_id_centro_poblado: int = None,
        p_id_ambito: int = None,
        p_nombre_categoria: str = None,
        p_fecha_ingreso: str = None,
        p_page: int = 1,
        p_page_size: int = 10,
        p_recepcionada: bool = None  # Se agrega el parámetro de filtrado
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""
                SELECT public.fn_documentos_get_documentos_recibidos_by_area_id(
                    :p_area_destino_id,
                    :p_search_document,
                    :p_id_caserio,
                    :p_id_centro_poblado,
                    :p_id_ambito,
                    :p_nombre_categoria,
                    :p_fecha_ingreso,
                    :p_page,
                    :p_page_size,
                    :p_recepcionada  -- Se incluye el nuevo parámetro en la consulta
                )
            """)
            connection = session.connection()
            result = connection.execute(query, {
                "p_area_destino_id": p_area_destino_id,
                "p_search_document": p_search_document,
                "p_id_caserio": p_id_caserio,
                "p_id_centro_poblado": p_id_centro_poblado,
                "p_id_ambito": p_id_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso,
                "p_page": p_page,
                "p_page_size": p_page_size,
                "p_recepcionada": p_recepcionada  # Se pasa el nuevo parámetro
            }).scalar()

            if result:
                return result
            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": p_page,
                        "page_size": p_page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }

    @staticmethod
    def get_rejected_documents_by_area_id(
        p_area_destino_id: int,
        p_search_document: int = None,
        p_id_caserio: int = None,
        p_id_centro_poblado: int = None,
        p_id_ambito: int = None,
        p_nombre_categoria: str = None,
        p_fecha_ingreso: str = None,
        p_page: int = 1,
        p_page_size: int = 10,
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""
                SELECT public.fn_documentos_get_documentos_rechazados_by_area_id(
                    :p_area_destino_id,
                    :p_search_document,
                    :p_id_caserio,
                    :p_id_centro_poblado,
                    :p_id_ambito,
                    :p_nombre_categoria,
                    :p_fecha_ingreso,
                    :p_page,
                    :p_page_size
                )
            """)
            connection = session.connection()
            result = connection.execute(query, {
                "p_area_destino_id": p_area_destino_id,
                "p_search_document": p_search_document,
                "p_id_caserio": p_id_caserio,
                "p_id_centro_poblado": p_id_centro_poblado,
                "p_id_ambito": p_id_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso,
                "p_page": p_page,
                "p_page_size": p_page_size
            }).scalar()

            if result:
                return result
            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": p_page,
                        "page_size": p_page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }

    @staticmethod
    def search_entered_documents(
            p_page: int,
            p_page_size: int,
            p_dni: Optional[int] = None,
            p_nombre_caserio: Optional[str] = None,
            p_nombre_centro_poblado: Optional[str] = None,
            p_nombre_ambito: Optional[str] = None,
            p_nombre_categoria: Optional[str] = None,
            p_fecha_ingreso: Optional[date] = None
        ) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text(
                """SELECT fn_buscar_documentos_ingresados_paginated(
                :p_dni,
                :p_nombre_caserio, 
                :p_nombre_centro_poblado, 
                :p_nombre_ambito, 
                :p_nombre_categoria, 
                :p_fecha_ingreso, 
                :p_page, 
                :p_page_size
                )"""
            )
            connection = session.connection()
            result = connection.execute(query, {
                "p_page": p_page,
                "p_page_size": p_page_size,
                "p_dni": p_dni,
                "p_nombre_caserio": p_nombre_caserio,
                "p_nombre_centro_poblado": p_nombre_centro_poblado,
                "p_nombre_ambito": p_nombre_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso
            }).scalar()

            if result:
                return result

            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": p_page,
                        "page_size": p_page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }
