from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, func, or_
from src.db.database import engine
from src.model.entity.categoria import Categoria

class CategoriaRepository:

    @staticmethod
    def add_categoria(categoria: Categoria) -> Categoria:
        with Session(engine) as session:
            session.add(categoria)
            session.commit()
            session.refresh(categoria)
        return categoria


    @staticmethod
    def get_all() -> List[Categoria]:
        with Session(engine) as session:
            categorias = session.exec(select(Categoria)).all()
        return categorias


    @staticmethod
    def update_categoria(categoria: Categoria) -> Categoria:
        with Session(engine) as session:
            session.add(categoria)
            session.commit()
            session.refresh(categoria)
        return categoria


    @staticmethod
    def delete_by_id(categoria_id: int) -> None:
        with Session(engine) as session:
            categoria = session.get(Categoria, categoria_id)
            if categoria:
                session.delete(categoria)
                session.commit()


    @staticmethod
    def get_by_id(categoria_id: int) -> Optional[Categoria]:
        with Session(engine) as session:
            categoria = session.get(Categoria, categoria_id)
        return categoria


    @staticmethod
    def exists(nombre_categoria: str) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Categoria).where(Categoria.nombre_categoria == nombre_categoria)).first() is not None
        return exists


    @staticmethod
    def find_by_string(search_string: str) -> List[Categoria]:
        with Session(engine) as session:
            search_filter = or_(
                Categoria.nombre_categoria.contains(search_string)
            )
            categorias = session.exec(select(Categoria).where(search_filter)).all()
        return categorias



    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            categorias = session.exec(
                select(Categoria)
                .order_by(Categoria.id)
                .offset(offset)
                .limit(page_size)
            ).all()
            total_items = session.exec(select(func.count()).select_from(Categoria)).first()
            total_pages = (total_items + page_size - 1) // page_size

        return {
            "data": categorias,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }