from pydantic import BaseModel, ConfigDict
from datetime import date

class TorneioBase(BaseModel):
    nome: str
    organizador: str
    data_inicio: date
    descricao: str | None = None
    formato: str | None = None

    model_config = ConfigDict(from_attributes=True)

class TorneioCreate(TorneioBase):
    pass

class TorneioResponse(TorneioBase):
    id: int
    capa: str | None = None

    model_config = ConfigDict(from_attributes=True)
