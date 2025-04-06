from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    gols = Column(Integer, default=0)
    time_id = Column(Integer, ForeignKey('times.id'), nullable=False)

    time = relationship("Time", back_populates="jogadores")
