from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schema para Time
class TimeBase(BaseModel):
    nome: str
    lugar: str

class TimeCreate(TimeBase):
    pass

class TimeResponse(TimeBase):
    id: int

    class Config:
        orm_mode = True

# Schema para Jogador
class JogadorBase(BaseModel):
    nome: str
    posicao: str
    gols: int

class JogadorCreate(JogadorBase):
    time_id: int

class JogadorResponse(JogadorBase):
    id: int
    time_id: int

    class Config:
        orm_mode = True

# Schema para Partida
class PartidaBase(BaseModel):
    data: datetime
    gols_time1: int
    gols_time2: int
    time1_id: int
    time2_id: int

class PartidaCreate(PartidaBase):
    pass

class PartidaResponse(PartidaBase):
    id: int

    class Config:
        orm_mode = True
