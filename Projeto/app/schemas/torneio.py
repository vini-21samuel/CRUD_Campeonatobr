from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class TorneioBase(BaseModel):
    nome: str
    organizador: str
    data_inicio: date
    descricao: Optional[str] = None
    formato: str
    numGrupos: Optional[int] = None  # Novo campo
    numClassificados: Optional[int] = None  # Novo campo

    model_config = ConfigDict(from_attributes=True)

class TorneioCreate(TorneioBase):
    pass

class TorneioUpdate(BaseModel):
    nome: Optional[str] = None
    organizador: Optional[str] = None
    data_inicio: Optional[date] = None
    descricao: Optional[str] = None
    formato: Optional[str] = None
    numGrupos: Optional[int] = None  # Novo campo
    numClassificados: Optional[int] = None  # Novo campo
    capa: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TorneioResponse(TorneioBase):
    id: int
    capa: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)