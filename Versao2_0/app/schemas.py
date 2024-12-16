from pydantic import BaseModel
from typing import List
from datetime import datetime
from datetime import date

# Schema para Jogador
class JogadorBase(BaseModel):
    nome: str
    posicao: str
    gols: int

class JogadorCreate(BaseModel):
    nome: str
    posicao: str
    gols: int = 0  # Define gols com valor padrão 0, para que não seja obrigatório
    time_id: int

class JogadorResponse(BaseModel):
    id: int
    nome: str
    posicao: str
    time_id: int

    class Config:
        orm_mode = True

# Modelo Time
class TimeBase(BaseModel):  # Agora existe a classe TimeBase para criação
    nome: str
    lugar: str

class TimeCreate(TimeBase):  # TimeCreate herda de TimeBase
    pass

class TimeResponse(BaseModel):
    id: int
    nome: str
    lugar: str
    jogadores: List[JogadorResponse]  # Lista de jogadores
    
    class Config:
        orm_mode = True

# Modelo Partida
class PartidaBase(BaseModel):
    time1_id: int
    time2_id: int
    data: date
    resultado: str | None = None  # O resultado pode ser None (não preenchido)

class PartidaCreate(PartidaBase):
    pass

class PartidaResponse(BaseModel):
    id: int
    time1_id: int
    time2_id: int
    data: date
    resultado: str | None
    time1: 'TimeResponse'  # Presumindo que você tem um schema TimeResponse para os times
    time2: 'TimeResponse'

    class Config:
        orm_mode = True