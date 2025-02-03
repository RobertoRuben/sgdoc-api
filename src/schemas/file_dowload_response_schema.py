from typing import Optional
from pydantic import BaseModel

class ResponseHeaders(BaseModel):
    content_disposition: str
    content_type: str
    date: str
    server: str
    transfer_encoding: Optional[str] = None

class FileDownloadResponseSchema(BaseModel):
    code: int
    details: str
    response_body: str
    response_headers: ResponseHeaders