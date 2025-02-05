from typing import Optional, Dict, Any, Tuple
from sqlmodel import Session, select, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.documento import Documento


class DocumentoRepository:

    @staticmethod
    def add_documentos(documento: Documento) -> Documento:
        with Session(engine) as session:
            try:
                session.add(documento)
                session.commit()
                session.refresh(documento)
                return documento
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al intentar agregar un documento") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al intentar agregar un documento") from e


    @staticmethod
    def update_document(documento: Documento) -> Documento:
        with Session(engine) as session:
            try:
                session.add(documento)
                session.commit()
                session.refresh(documento)
                return documento
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al intentar actualizar un documento") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al intentar actualizar un documento") from e


    @staticmethod
    def get_document_by_id(documento_id: int) -> Documento:
        with Session(engine) as session:
            try:
                documento = session.exec(select(Documento).where(Documento.id == documento_id)).first()
                return documento
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener un documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener un documento") from e


    @staticmethod
    def delete_document_by_id(documento_id: int):
        with Session(engine) as session:
            try:
                documento = session.get(Documento, documento_id)
                if documento:
                    session.delete(documento)
                    session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al intentar eliminar un documento") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al intentar eliminar un documento") from e


    @staticmethod
    def exists_by_id(documento_id: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Documento).where(Documento.id == documento_id)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar verificar la existencia de un documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar verificar la existencia de un documento") from e


    @staticmethod
    def exists_by_name(documento_name: str) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Documento).where(Documento.nombre == documento_name)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar verificar la existencia de un documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar verificar la existencia de un documento") from e


    @staticmethod
    def get_document_bytes_and_name_by_id(documento_id: int) -> Tuple[Optional[bytes], Optional[str]]:
        with Session(engine) as session:
            try:
                result = session.exec(
                    select(Documento.documento_bytes, Documento.nombre)
                    .where(Documento.id == documento_id)
                ).first()
                if result:
                    documento_bytes, nombre = result
                    return documento_bytes, nombre
                return None, None
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener el documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener el documento") from e


    @staticmethod
    def get_documents_by_current_date(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        with Session(engine) as session:
            try:
                query = text("""SELECT fn_documentos_listar_por_fecha_actual_paginado(:page, :page_size)""")
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener los documentos por fecha actual") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener los documentos por fecha actual") from e


    @staticmethod
    def get_all_documents_paginated(p_page: int, p_page_size: int) -> Dict[str, Any]:
        with Session(engine) as session:
            try:
                query = text("""SELECT fn_documentos_listar_paginado(:p_page, :p_page_size)""")
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener los documentos paginados") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener los documentos paginados") from e


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
            try:
                query = text("""
                    SELECT public.fn_documentos_listar_enviados_por_area_origen_id(
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener los documentos enviados por area origen") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener los documentos enviados por area origen") from e


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
        p_recepcionada: bool = None
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            try:
                query = text("""
                    SELECT public.fn_documentos_listar_recibidos_por_area_destino_id(
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
                    "p_recepcionada": p_recepcionada
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener los documentos recibidos por area destino") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener los documentos recibidos por area destino") from e


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
            try:
                query = text("""
                    SELECT public.fn_documentos_listar_rechazados_por_area_destino_id(
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener los documentos rechazados por area destino") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener los documentos rechazados por area destino") from e


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
            try:
                query = text(
                    """SELECT fn_documentos_buscar_ingresados_paginado(
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar buscar los documentos ingresados") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar buscar los documentos ingresados") from e


    @staticmethod
    def get_total_unconfirmed_received_documents_today(p_area_destino_id: int) -> int:
        with Session(engine) as session:
            try:
                query = text("SELECT fn_documentos_total_recibidos_no_confirmados_hoy(:p_area_destino_id)")
                connection = session.connection()
                result = connection.execute(query, {"p_area_destino_id": p_area_destino_id}).scalar()

                return result if result is not None else 0

            except SQLAlchemyError as e:
                raise DatabaseException("Error al intentar obtener el total de documentos no confirmados") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al intentar obtener documentos no confirmados") from e
