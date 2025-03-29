from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import List
from datetime import date
from marshmallow import Schema, fields
from pydantic import BaseModel
from typing import List

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

class TimeBase(BaseModel):
    id: int
    nome: str
    lugar: str

class TimeCreate(TimeBase):
    pass

class TimeResponse(TimeBase):
    id: int
    nome: str
    lugar: str

    class Config:
        orm_mode = True


# Modelo Partida
class PartidaBase(BaseModel):
    time1_id: int
    time2_id: int
    data: date
    resultado: str | None = None

class PartidaCreate(PartidaBase):
    pass

class PartidaResponse(BaseModel):
    id: int
    data: str  # Altere para string
    resultado: str
    time1_nome: str
    time2_nome: str

    @field_validator("data", mode="before")
    def formatar_data(cls, v):
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")  # Converte date para string
        return v
    

    class Config:
        orm_mode = True


class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True 
    

class UsuarioLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True 

class Token(BaseModel):
    access_token: str
    token_type: str

class Usuario(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True 

class TorneioBase(BaseModel):
    nome: str
    organizador: str
    data_inicio: date
    descricao: str | None = None
    formato: str | None = None

    model_config = ConfigDict(from_attributes=True)  # 🚀 Corrige erros de conversão Pydantic

class TorneioCreate(TorneioBase):
    pass

class TorneioResponse(TorneioBase):
    id: int
    capa: str | None = None

    model_config = ConfigDict(from_attributes=True)