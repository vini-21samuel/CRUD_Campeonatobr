from pydantic import BaseModel
from typing import Optional

class PartidaCreate(BaseModel):
    time1_id: int
    time2_id: int
    data: str  # Entrada como string no formato "YYYY-MM-DD"
    resultado: Optional[str] = None
    torneio_id: int

class PartidaUpdate(BaseModel):
    time1_id: Optional[int] = None
    time2_id: Optional[int] = None
    data: Optional[str] = None
    resultado: Optional[str] = None

class PartidaResponse(BaseModel):
    id: int
    time1_id: int
    time2_id: int
    time1_nome: str
    time2_nome: str
    time1_logo: Optional[str] = None
    time2_logo: Optional[str] = None
    data: str  # Saída como string no formato "YYYY-MM-DD"
    resultado: Optional[str] = None
    torneio_id: int

    class Config:
        orm_mode = True