from typing import Optional, Dict, Any, Tuple
from datetime import date
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Documento

class DocumentoRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_documentos(self, documento: Documento) -> Documento:
        try:
            self.session.add(documento)
            await self.session.commit()
            await self.session.refresh(documento)
            return documento
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al intentar agregar un documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al intentar agregar un documento",
                error_details=str(e)
            ) from e


    async def update_document(self, documento: Documento) -> Documento:
        try:
            self.session.add(documento)
            await self.session.commit()
            await self.session.refresh(documento)
            return documento
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al intentar actualizar un documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al intentar actualizar un documento",
                error_details=str(e)
            ) from e


    async def get_document_by_id(self, documento_id: int) -> Optional[Documento]:
        try:
            result = await self.session.exec(select(Documento).where(Documento.id == documento_id))
            documento = result.first()
            return documento
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al intentar obtener un documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al intentar obtener un documento",
                error_details=str(e)
            ) from e


    async def delete_document_by_id(self, documento_id: int) -> None:
        try:
            documento = await self.session.get(Documento, documento_id)
            if documento:
                await self.session.delete(documento)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al intentar eliminar un documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al intentar eliminar un documento",
                error_details=str(e)
            ) from e


    async def exists_by_id(self, documento_id: int) -> bool:
        try:
            documento = await self.session.get(Documento, documento_id)
            return documento is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al intentar verificar la existencia de un documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al intentar verificar la existencia de un documento",
                error_details=str(e)
            ) from e


    async def exists_by_name(self, documento_name: str) -> bool:
        try:
            result = await self.session.exec(select(Documento).where(Documento.nombre == documento_name))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al intentar verificar la existencia de un documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar verificar la existencia de un documento",
                error_details=str(e)
            ) from e


    async def get_document_bytes_and_name_by_id(self, documento_id: int) -> Tuple[Optional[bytes], Optional[str]]:
        try:
            result = await self.session.exec(
                select(Documento.documento_bytes, Documento.nombre).where(Documento.id == documento_id)
            )
            res = result.first()
            if res:
                documento_bytes, nombre = res
                return documento_bytes, nombre
            return None, None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al intentar obtener el documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener el documento",
                error_details=str(e)
            ) from e


    async def get_documents_by_current_date(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            query = text("SELECT fn_documentos_listar_por_fecha_actual_paginado(:page, :page_size)")
            result = await self.session.execute(query, {"page": page, "page_size": page_size})
            res = result.scalar()
            if res:
                return res
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
            raise DatabaseException(
                "Error al intentar obtener los documentos por fecha actual",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener los documentos por fecha actual",
                error_details=str(e)
            ) from e


    async def get_all_documents_paginated(self, p_page: int, p_page_size: int) -> Dict[str, Any]:
        try:
            query = text("SELECT fn_documentos_listar_paginado(:p_page, :p_page_size)")
            result = await self.session.execute(query, {"p_page": p_page, "p_page_size": p_page_size})
            res = result.scalar()
            if res:
                return res
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
            raise DatabaseException(
                "Error al intentar obtener los documentos paginados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener los documentos paginados",
                error_details=str(e)
            ) from e


    async def get_sent_documents_by_area_id(
        self,
        p_area_origen_id: int,
        p_search_document: Optional[int] = None,
        p_id_caserio: Optional[int] = None,
        p_id_centro_poblado: Optional[int] = None,
        p_id_ambito: Optional[int] = None,
        p_nombre_categoria: Optional[str] = None,
        p_fecha_ingreso: Optional[str] = None,
        p_page: int = 1,
        p_page_size: int = 10
    ) -> Dict[str, Any]:
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
            result = await self.session.execute(query, {
                "p_area_origen_id": p_area_origen_id,
                "p_search_document": p_search_document,
                "p_id_caserio": p_id_caserio,
                "p_id_centro_poblado": p_id_centro_poblado,
                "p_id_ambito": p_id_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso,
                "p_page": p_page,
                "p_page_size": p_page_size
            })
            res = result.scalar()
            if res:
                return res
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
            raise DatabaseException(
                "Error al intentar obtener los documentos enviados por area origen",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener los documentos enviados por area origen",
                error_details=str(e)
            ) from e


    async def get_received_documents_by_area_id(
        self,
        p_area_destino_id: int,
        p_search_document: Optional[int] = None,
        p_id_caserio: Optional[int] = None,
        p_id_centro_poblado: Optional[int] = None,
        p_id_ambito: Optional[int] = None,
        p_nombre_categoria: Optional[str] = None,
        p_fecha_ingreso: Optional[str] = None,
        p_page: int = 1,
        p_page_size: int = 10,
        p_recepcionada: Optional[bool] = None
    ) -> Dict[str, Any]:
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
                    :p_recepcionada
                )
            """)
            result = await self.session.execute(query, {
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
            })
            res = result.scalar()
            if res:
                return res
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
            raise DatabaseException(
                "Error al intentar obtener los documentos recibidos por area destino",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener los documentos recibidos por area destino",
                error_details=str(e)
            ) from e


    async def get_rejected_documents_by_area_id(
        self,
        p_area_destino_id: int,
        p_search_document: Optional[int] = None,
        p_id_caserio: Optional[int] = None,
        p_id_centro_poblado: Optional[int] = None,
        p_id_ambito: Optional[int] = None,
        p_nombre_categoria: Optional[str] = None,
        p_fecha_ingreso: Optional[str] = None,
        p_page: int = 1,
        p_page_size: int = 10,
    ) -> Dict[str, Any]:
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
            result = await self.session.execute(query, {
                "p_area_destino_id": p_area_destino_id,
                "p_search_document": p_search_document,
                "p_id_caserio": p_id_caserio,
                "p_id_centro_poblado": p_id_centro_poblado,
                "p_id_ambito": p_id_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso,
                "p_page": p_page,
                "p_page_size": p_page_size
            })
            res = result.scalar()

            if res:
                return res
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
            raise DatabaseException(
                "Error al intentar obtener los documentos rechazados por area destino",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener los documentos rechazados por area destino",
                error_details=str(e)
            ) from e


    async def search_entered_documents(
        self,
        p_page: int,
        p_page_size: int,
        p_dni: Optional[int] = None,
        p_nombre_caserio: Optional[str] = None,
        p_nombre_centro_poblado: Optional[str] = None,
        p_nombre_ambito: Optional[str] = None,
        p_nombre_categoria: Optional[str] = None,
        p_fecha_ingreso: Optional[date] = None
    ) -> Dict[str, Any]:
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
            result = await self.session.execute(query, {
                "p_page": p_page,
                "p_page_size": p_page_size,
                "p_dni": p_dni,
                "p_nombre_caserio": p_nombre_caserio,
                "p_nombre_centro_poblado": p_nombre_centro_poblado,
                "p_nombre_ambito": p_nombre_ambito,
                "p_nombre_categoria": p_nombre_categoria,
                "p_fecha_ingreso": p_fecha_ingreso
            })
            res = result.scalar()
            if res:
                return res
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
            raise DatabaseException(
                "Error al intentar buscar los documentos ingresados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar buscar los documentos ingresados",
                error_details=str(e)
            ) from e


    async def get_total_unconfirmed_received_documents_today(self, p_area_destino_id: int) -> int:
        try:
            query = text("SELECT fn_documentos_total_recibidos_no_confirmados_hoy(:p_area_destino_id)")
            result = await self.session.execute(query, {"p_area_destino_id": p_area_destino_id})
            res = result.scalar()
            return res if res is not None else 0
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al intentar obtener el total de documentos no confirmados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al intentar obtener documentos no confirmados",
                error_details=str(e)
            ) from e
