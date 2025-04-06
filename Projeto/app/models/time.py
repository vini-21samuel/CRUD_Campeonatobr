from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Time(Base):
    __tablename__ = 'times'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    lugar = Column(String, nullable=False)
    torneio_id = Column(Integer, ForeignKey("torneios.id"), nullable=True)
    logo = Column(String, nullable=True)

    jogadores = relationship("Jogador", back_populates="time")
    partidas_time1 = relationship("Partida", foreign_keys="[Partida.time1_id]", back_populates="time1")
    partidas_time2 = relationship("Partida", foreign_keys="[Partida.time2_id]", back_populates="time2")
    torneio = relationship("Torneio", back_populates="times")
