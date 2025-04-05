from pydantic import BaseModel
from typing import Optional
from app.schemas.time import TimeResponse

class JogadorBase(BaseModel):
    nome: str
    posicao: str
    gols: int

class JogadorCreate(JogadorBase):
    id: int
    time_id: int

class JogadorResponse(JogadorBase):
    id: int
    time: TimeResponse

    class Config:
        orm_mode = True
