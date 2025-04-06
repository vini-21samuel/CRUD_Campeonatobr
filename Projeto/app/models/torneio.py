from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class Torneio(Base):
    __tablename__ = "torneios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    organizador = Column(String(100), nullable=False)
    data_inicio = Column(Date, nullable=False)
    descricao = Column(Text, nullable=True)
    formato = Column(String(255), nullable=True)
    capa = Column(String, nullable=True)

    times = relationship("Time", back_populates="torneio")

    def __repr__(self):
        return f"<Torneio(nome={self.nome}, organizador={self.organizador}, data_inicio={self.data_inicio})>"
