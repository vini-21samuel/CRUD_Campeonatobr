from pydantic import BaseModel
from typing import Optional

class TimeBase(BaseModel):
    nome: str
    lugar: str

class TimeCreate(TimeBase):
    torneio_id: int

class TimeResponse(TimeBase):
    id: int
    torneio_id: Optional[int] = None
    logo: Optional[str] = None

    class Config:
        orm_mode = True
