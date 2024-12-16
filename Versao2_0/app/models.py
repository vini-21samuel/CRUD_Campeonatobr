# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Date
from datetime import datetime

# Modelo de Time
class Time(Base):
    __tablename__ = 'times'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    lugar = Column(String)


    
    jogadores = relationship("Jogador", back_populates="time")
    partidas_time1 = relationship("Partida", foreign_keys="[Partida.time1_id]", back_populates="time1")
    partidas_time2 = relationship("Partida", foreign_keys="[Partida.time2_id]", back_populates="time2")

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    posicao = Column(String)
    gols = Column(Integer, default=0) 
    time_id = Column(Integer, ForeignKey('times.id'))  # Chave estrangeira para 'times'

    # Relacionamento com time
    time = relationship("Time", back_populates="jogadores")
    # outros campos...


# Modelo Partida

class Partida(Base):
    __tablename__ = 'partidas'
    
    id = Column(Integer, primary_key=True, index=True)
    time1_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    time2_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    data = Column(Date, nullable=False)
    resultado = Column(String(255), nullable=True)

    time1 = relationship("Time", foreign_keys=[time1_id], back_populates="partidas_time1")
    time2 = relationship("Time", foreign_keys=[time2_id], back_populates="partidas_time2")

