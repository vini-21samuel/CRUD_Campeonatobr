from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Partida(Base):
    __tablename__ = 'partidas'

    id = Column(Integer, primary_key=True)
    time1_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    time2_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    data = Column(Date, nullable=False)
    resultado = Column(String, nullable=True)

    time1 = relationship('Time', foreign_keys=[time1_id], back_populates="partidas_time1")
    time2 = relationship('Time', foreign_keys=[time2_id], back_populates="partidas_time2")
