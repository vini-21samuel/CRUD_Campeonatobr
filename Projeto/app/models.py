from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Date
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

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
    time_id = Column(Integer, ForeignKey('times.id'))


    # Relacionamento com time
    time = relationship("Time", back_populates="jogadores")

# Modelo Partida
class Partida(Base):
    __tablename__ = "partidas"
    id = Column(Integer, primary_key=True, index=True)
    time1_id = Column(Integer, ForeignKey("times.id"))
    time2_id = Column(Integer, ForeignKey("times.id"))
    resultado = Column(String)
    data = Column(Date)

    time1 = relationship("Time", foreign_keys=[time1_id], lazy="joined")
    time2 = relationship("Time", foreign_keys=[time2_id], lazy="joined")
