from sqlalchemy import Column, Integer, String
from database import Base

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    lugar = Column(String, nullable=False)

class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    time_id = Column(Integer, nullable=False)
    gols = Column(Integer, default=0)
