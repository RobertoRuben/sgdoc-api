from pydantic import BaseModel
from typing import List, Any

class PaginationMeta(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int

class PaginatedResponse(BaseModel):
    data: List[Any]
    pagination: PaginationMeta
