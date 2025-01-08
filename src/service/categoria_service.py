from typing import List, Dict, Any
from fastapi import HTTPException, Depends
from src.model.entity.categoria import Categoria
from src.dto.categoria_request import CategoriaRequest
from src.dto.categoria_response import CategoriaResponse
from src.repository.categoria_repository import CategoriaRepository

class CategoriaService:

    def __init__(self, categoria_repository: CategoriaRepository = Depends()):
        self.categoria_repository = categoria_repository


    def add_categoria(self, categoria_request: CategoriaRequest) -> CategoriaResponse:
        if self.categoria_repository.exists(categoria_request.nombre_categoria):
            raise HTTPException(status_code=400, detail="La categoria ya existe en la base de datos")

        new_categoria = Categoria(
            nombre_categoria=categoria_request.nombre_categoria
        )

        created_categoria = self.categoria_repository.add_categoria(new_categoria)

        return CategoriaResponse(
            id=created_categoria.id,
            nombre_categoria=created_categoria.nombre_categoria
        )


    def get_categorias(self) -> List[CategoriaResponse]:
        categorias = self.categoria_repository.get_all()

        return [CategoriaResponse(
            id=categoria.id,
            nombre_categoria=categoria.nombre_categoria
        ) for categoria in categorias]


    def update_categoria(self, categoria_id: int, categoria_request: CategoriaRequest) -> CategoriaResponse:
        categoria = self.categoria_repository.get_by_id(categoria_id)

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        if self.categoria_repository.exists(categoria_request.nombre_categoria):
            raise HTTPException(status_code=400, detail="La categoria ya existe en la base de datos")

        categoria.nombre_categoria = categoria_request.nombre_categoria

        updated_categoria = self.categoria_repository.update_categoria(categoria)

        return CategoriaResponse(
            id=updated_categoria.id,
            nombre_categoria=updated_categoria.nombre_categoria
        )


    def delete_categoria(self, categoria_id: int):
        categoria = self.categoria_repository.get_by_id(categoria_id)

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        self.categoria_repository.delete_by_id(categoria_id)


    def find_categoria_by_string(self, nombre_categoria: str) -> List[CategoriaResponse]:
        categorias = self.categoria_repository.find_by_string(nombre_categoria)

        if not categorias:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        return [CategoriaResponse(
            id=categoria.id,
            nombre_categoria=categoria.nombre_categoria
        ) for categoria in categorias]



    def get_categorias_by_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        return self.categoria_repository.get_all_pagination(page, page_size)


    def get_categoria_by_id(self, categoria_id: int) -> CategoriaResponse:
        categoria = self.categoria_repository.get_by_id(categoria_id)

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        return CategoriaResponse(
            id=categoria.id,
            nombre_categoria=categoria.nombre_categoria
        )
