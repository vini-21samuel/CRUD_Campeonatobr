from pydantic import BaseModel

class TimeBase(BaseModel):
    nome: str
    lugar: str

class TimeCreate(TimeBase):
    pass

class TimeResponse(TimeBase):
    id: int

    class Config:
        orm_mode = True

class JogadorBase(BaseModel):
    nome: str
    posicao: str
    time_id: int
    gols: int = 0

class JogadorCreate(JogadorBase):
    pass

class JogadorResponse(JogadorBase):
    id: int

    class Config:
        orm_mode = True