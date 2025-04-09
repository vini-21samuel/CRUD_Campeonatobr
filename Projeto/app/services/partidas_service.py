from sqlalchemy.orm import Session
from app.models.partida import Partida
from app.models.time import Time
from app.schemas.partida import PartidaCreate, PartidaResponse, PartidaUpdate
from typing import List, Optional
from fastapi import HTTPException

class PartidaService:
    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate):
        db_partida = Partida(**partida.dict())
        db.add(db_partida)
        db.commit()
        db.refresh(db_partida)
        return PartidaService._map_to_response(db, db_partida)

    @staticmethod
    def listar_partidas(db: Session, torneio_id: Optional[int] = None):
        query = db.query(Partida)
        if torneio_id:
            query = query.filter(Partida.torneio_id == torneio_id)
        partidas = query.all()
        return [PartidaService._map_to_response(db, partida) for partida in partidas]

    @staticmethod
    def obter_partida(db: Session, partida_id: int):
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        return PartidaService._map_to_response(db, partida)

    @staticmethod
    def atualizar_partida(db: Session, partida_id: int, partida: PartidaUpdate):
        db_partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not db_partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        for key, value in partida.dict(exclude_unset=True).items():
            setattr(db_partida, key, value)
        db.commit()
        db.refresh(db_partida)
        return PartidaService._map_to_response(db, db_partida)

    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        db_partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not db_partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        db.delete(db_partida)
        db.commit()

    @staticmethod
    def _map_to_response(db: Session, partida: Partida) -> PartidaResponse:
        time1 = db.query(Time).filter(Time.id == partida.time1_id).first()
        time2 = db.query(Time).filter(Time.id == partida.time2_id).first()
        return PartidaResponse(
            id=partida.id,
            time1_id=partida.time1_id,
            time2_id=partida.time2_id,
            time1_nome=time1.nome if time1 else "Desconhecido",
            time2_nome=time2.nome if time2 else "Desconhecido",
            time1_logo=time1.logo if time1 else None,
            time2_logo=time2.logo if time2 else None,
            data=partida.data.strftime("%Y-%m-%d"),  # Converte datetime.date para string
            resultado=partida.resultado,
            torneio_id=partida.torneio_id
        )