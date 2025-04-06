from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import date

class PartidaBase(BaseModel):
    time1_id: int
    time2_id: int
    data: date
    resultado: Optional[str] = None
    torneio_id: int

class PartidaCreate(PartidaBase):
    pass

class PartidaUpdate(PartidaBase):
    pass

class PartidaResponse(BaseModel):
    id: int
    time1_nome: str
    time2_nome: str
    time1_logo: Optional[str] = None
    time2_logo: Optional[str] = None
    data: str
    resultado: Optional[str] = None

    @field_validator("data", mode="before")
    def formatar_data(cls, v):
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")
        return v

    class Config:
        orm_mode = True