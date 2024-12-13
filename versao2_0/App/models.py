from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

# Modelo para "Times"
class Time(Base):
    __tablename__ = 'times'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    lugar = Column(String, nullable=False)

    jogadores = relationship("Jogador", back_populates="time")
    partidas = relationship("Partida", back_populates="time")

# Modelo para "Jogadores"
class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    gols = Column(Integer, default=0)
    time_id = Column(Integer, ForeignKey("times.id"))

    time = relationship("Time", back_populates="jogadores")

# Modelo para "Partidas"
class Partida(Base):
    __tablename__ = 'partidas'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, nullable=False)
    time1_id = Column(Integer, ForeignKey("times.id"))
    time2_id = Column(Integer, ForeignKey("times.id"))
    gols_time1 = Column(Integer, default=0)
    gols_time2 = Column(Integer, default=0)

    time1 = relationship("Time", foreign_keys=[time1_id], back_populates="partidas")
    time2 = relationship("Time", foreign_keys=[time2_id], back_populates="partidas")
