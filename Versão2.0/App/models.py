from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    lugar = Column(String, nullable=False)

    jogadores = relationship("Jogador", back_populates="time")

class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    gols = Column(Integer, default=0)
    time_id = Column(Integer, ForeignKey("times.id"))

    time = relationship("Time", back_populates="jogadores")
