from typing import List, Dict, Any
from fastapi import Depends
from src.exception import ConflictException, NotFoundException, InternalServerException
from src.model.entity import Categoria
from src.dto import CategoriaDocumentoRequestDTO, CategoriaDocumentoResponseDTO
from src.repository import CategoriaDocumentoRepository
from src.service import CategoriaDocumentoService

class CategoriaDocumentoServiceImp(CategoriaDocumentoService):
    def __init__(self, categoria_repository: CategoriaDocumentoRepository = Depends()):
        self.categoria_repository = categoria_repository


    async def add_categoria_documento(self, categoria_request: CategoriaDocumentoRequestDTO) -> CategoriaDocumentoResponseDTO:
        try:
            exists = await self.categoria_repository.exists(categoria_request.nombre_categoria)
            if exists:
                raise ConflictException("La categoria de documento ya existe en la base de datos")

            new_categoria = Categoria(
                nombre_categoria=categoria_request.nombre_categoria
            )

            created_categoria = await self.categoria_repository.add_categoria(new_categoria)

            return CategoriaDocumentoResponseDTO(
                id=created_categoria.id,
                nombre_categoria=created_categoria.nombre_categoria
            )
        except ConflictException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear la categoria de documento",
                error_details=str(e)
            ) from e


    async def get_all_categorias_documento(self) -> List[CategoriaDocumentoResponseDTO]:
        try:
            categorias = await self.categoria_repository.get_all_categorias()
            return [
                CategoriaDocumentoResponseDTO(
                    id=categoria.id,
                    nombre_categoria=categoria.nombre_categoria
                )
                for categoria in categorias
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las categorias de documento",
                error_details=str(e)
            ) from e


    async def update_categoria_documento(self, categoria_id: int, categoria_request: CategoriaDocumentoRequestDTO) -> CategoriaDocumentoResponseDTO:
        try:
            categoria = await self.categoria_repository.get_by_id(categoria_id)
            if not categoria:
                raise NotFoundException("Categoria de documento no encontrada")

            if categoria.nombre_categoria == categoria_request.nombre_categoria:
                return CategoriaDocumentoResponseDTO(
                    id=categoria.id,
                    nombre_categoria=categoria.nombre_categoria
                )

            exists = await self.categoria_repository.exists(categoria_request.nombre_categoria)
            if exists:
                raise ConflictException("La categoria ya existe en la base de datos")

            categoria.nombre_categoria = categoria_request.nombre_categoria

            updated_categoria = await self.categoria_repository.update_categoria(categoria)

            return CategoriaDocumentoResponseDTO(
                id=updated_categoria.id,
                nombre_categoria=updated_categoria.nombre_categoria
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar la categoria de documento",
                error_details=str(e)
            ) from e


    async def delete_categoria_documento_by_id(self, categoria_id: int) -> None:
        try:
            categoria = await self.categoria_repository.get_by_id(categoria_id)
            if not categoria:
                raise NotFoundException("Categoria de documento no encontrada")

            await self.categoria_repository.delete_by_id(categoria_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar la categoria de documento",
                error_details=str(e)
            ) from e


    async def find_categoria_documento(self, nombre_categoria: str) -> List[CategoriaDocumentoResponseDTO]:
        try:
            categorias = await self.categoria_repository.find_by_string(nombre_categoria)
            return [
                CategoriaDocumentoResponseDTO(
                    id=categoria.id,
                    nombre_categoria=categoria.nombre_categoria
                )
                for categoria in categorias
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar la categoria de documento",
                error_details=str(e)
            ) from e


    async def get_categorias_documento_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.categoria_repository.get_all_pagination(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las categorias de documento paginadas",
                error_details=str(e)
            ) from e


    async def get_categoria_documento_by_id(self, categoria_id: int) -> CategoriaDocumentoResponseDTO:
        try:
            categoria = await self.categoria_repository.get_by_id(categoria_id)
            if not categoria:
                raise NotFoundException("Categoria no encontrada")
            return CategoriaDocumentoResponseDTO(
                id=categoria.id,
                nombre_categoria=categoria.nombre_categoria
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener la categoria de documento",
                error_details=str(e)
            ) from e
