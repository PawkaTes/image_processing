from pydantic import BaseModel
from datetime import datetime

class ImageCreate(BaseModel):
    title: str

class ImageResponse(BaseModel):
    id: int
    title: str
    file_path: str
    upload_date: datetime
    resolution: str
    size: int

    class Config:
        orm_mode = True
