from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.database import Base, engine
from datetime import datetime

# Modelo de Usuário
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
    nome = Column(String, nullable=False)
    lugar = Column(String, nullable=False)
    torneio_id = Column(Integer, ForeignKey("torneios.id"), nullable=True)  # Relacionamento com torneio

    jogadores = relationship("Jogador", back_populates="time")
    partidas_time1 = relationship("Partida", foreign_keys="[Partida.time1_id]", back_populates="time1")
    partidas_time2 = relationship("Partida", foreign_keys="[Partida.time2_id]", back_populates="time2")
    torneio = relationship("Torneio", back_populates="times")  # Relacionamento com Torneio

# Modelo de Jogador
class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    gols = Column(Integer, default=0)
    time_id = Column(Integer, ForeignKey('times.id'), nullable=False)

    # Relacionamento com Time
    time = relationship("Time", back_populates="jogadores")

# Modelo de Partida
class Partida(Base):
    __tablename__ = 'partidas'
    
    id = Column(Integer, primary_key=True)
    time1_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    time2_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    data = Column(Date, nullable=False)
    resultado = Column(String, nullable=True)

    time1 = relationship('Time', foreign_keys=[time1_id])
    time2 = relationship('Time', foreign_keys=[time2_id])



# Modelo de Torneio
class Torneio(Base):
    __tablename__ = "torneios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    organizador = Column(String(100), nullable=False)
    data_inicio = Column(Date, nullable=False)
    descricao = Column(Text, nullable=True)
    formato = Column(String(255), nullable=True)
    capa = Column(String, nullable=True)

    # Relacionamento com Time
    times = relationship("Time", back_populates="torneio")  

    def __repr__(self):
        return f"<Torneio(nome={self.nome}, organizador={self.organizador}, data_inicio={self.data_inicio})>"

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
