from pydantic import BaseModel
from typing import Optional, List

class TimeBase(BaseModel):
    nome: str
    lugar: str

class TimeCreate(TimeBase):
    pass

class TimeResponse(TimeBase):
    id: int
    jogadores: List["JogadorResponse"] = []

    class Config:
        orm_mode = True

class JogadorBase(BaseModel):
    nome: str
    posicao: str
    gols: int
    time_id: int

class JogadorCreate(JogadorBase):
    pass

class JogadorResponse(JogadorBase):
    id: int
    time: Optional[TimeResponse] = None

    class Config:
        orm_mode = True
