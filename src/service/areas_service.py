from typing import  List, Any, Dict
from fastapi import HTTPException, Depends
from src.dto.area_request import AreaRequest
from src.dto.area_response import AreaResponse
from src.model.entity.area import Area
from src.repository.area_repository import AreaRepository

class AreaService:

    def __init__(self, area_repository: AreaRepository = Depends()):
        self.area_repository = area_repository


    def add_area(self, area_request: AreaRequest) -> AreaResponse:
        if self.area_repository.exists(area_request.nombre_area):
            raise HTTPException(status_code=400, detail="El area ya existe")

        area = Area(
            nombre_area=area_request.nombre_area
        )

        area = self.area_repository.add_area(area)

        return AreaResponse(
            id=area.id,
            nombre_area=area.nombre_area
        )

    def get_all_areas(self) -> List[AreaResponse]:
        areas = self.area_repository.get_all_areas()

        return [
            AreaResponse(
                id=area.id,
                nombre_area=area.nombre_area
            ) for area in areas
        ]


    def update_area(self, area_id: int, area_request: AreaRequest) -> AreaResponse:
        area = self.area_repository.get_area_by_id(area_id)
        if not area:
            raise HTTPException(status_code=404, detail="Area no encontrada")

        if self.area_repository.exists(area_request.nombre_area):
            raise HTTPException(status_code=400, detail="El area ya existe")

        area.nombre_area = area_request.nombre_area

        area = self.area_repository.update_area(area)

        return AreaResponse(
            id=area.id,
            nombre_area=area.nombre_area
        )


    def delete_area_by_id(self, area_id: int) -> None:
        area = self.area_repository.get_area_by_id(area_id)
        if not area:
            raise HTTPException(status_code=404, detail="Area no encontrada")

        self.area_repository.delete_area_by_id(area_id)


    def find_areas_by_string(self, search_string: str) -> List[AreaResponse]:
        areas = self.area_repository.find_by_string(search_string)

        return [
            AreaResponse(
                id=area.id,
                nombre_area=area.nombre_area
            ) for area in areas
        ]


    def get_all_areas_by_pagination(self, page:int , page_size:int) ->Dict[str, Any]:
        return self.area_repository.get_all_pagination(page, page_size)