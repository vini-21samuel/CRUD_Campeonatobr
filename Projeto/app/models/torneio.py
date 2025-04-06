from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database.database import Base

class Torneio(Base):
    __tablename__ = 'torneios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    organizador = Column(String, nullable=False)
    data_inicio = Column(Date, nullable=False)
    formato = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    capa = Column(String, nullable=True)

    partidas = relationship('Partida', back_populates="torneio")
    times = relationship('Time', back_populates="torneio")