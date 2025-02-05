from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from datetime import date

# Schema para Jogador
class JogadorBase(BaseModel):
    nome: str
    posicao: str
    gols: int

class JogadorCreate(BaseModel):
    id: int  # Inclui o identificador no corpo
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
    id: int
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
    data: date  # Alterado para tipo `date`
    resultado: str | None = None

class PartidaCreate(PartidaBase):
    pass

class PartidaResponse(BaseModel):
    id: int  # O campo id deve ser obrigatório
    time1_id: int | None  # Permitir que seja nulo ou um inteiro
    time2_id: int | None
    data: str  # Mantemos como string
    resultado: str | None  # Permitir que seja nulo


    class Config:
        orm_mode = True 

class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Se estiver utilizando ORM, pode ser necessário configurar:
class Usuario(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True 