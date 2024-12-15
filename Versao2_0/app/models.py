from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Time(Base):
    __tablename__ = 'times'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    jogadores = relationship("Jogador", back_populates="time")  # Relacionamento explícito
    partidas = relationship("Partida", back_populates="time1")  # Relacionamento com partidas (time1)
    partidas_oponente = relationship("Partida", back_populates="time2")  # Relacionamento com partidas (time2)


class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    time_id = Column(Integer, ForeignKey("times.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    time = relationship("Time", back_populates="jogadores")  # Relacionamento explícito


class Partida(Base):
    __tablename__ = 'partidas'

    id = Column(Integer, primary_key=True, index=True)
    time1_id = Column(Integer, ForeignKey("times.id"), nullable=False)  # Time 1
    time2_id = Column(Integer, ForeignKey("times.id"), nullable=False)  # Time 2
    data = Column(Date, nullable=False)  # Data da partida
    placar_time1 = Column(Integer, nullable=True)  # Placar do Time 1
    placar_time2 = Column(Integer, nullable=True)  # Placar do Time 2
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    # Relacionamento com os times
    time1 = relationship("Time", foreign_keys=[time1_id], back_populates="partidas")
    time2 = relationship("Time", foreign_keys=[time2_id], back_populates="partidas_oponente")
