from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import alias
from app.models.partida import Partida
from app.schemas.partida import PartidaCreate, PartidaResponse, PartidaUpdate
from fastapi import HTTPException

class PartidaRepository:
    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate) -> PartidaResponse:
        db_partida = Partida(**partida.dict())
        db.add(db_partida)
        db.commit()
        db.refresh(db_partida)
        return PartidaResponse(
            id=db_partida.id,
            time1_nome=db_partida.time1.nome if db_partida.time1 else "Desconhecido",
            time2_nome=db_partida.time2.nome if db_partida.time2 else "Desconhecido",
            time1_logo=db_partida.time1.logo if db_partida.time1 else None,
            time2_logo=db_partida.time2.logo if db_partida.time2 else None,
            data=db_partida.data,
            resultado=db_partida.resultado
        )

    @staticmethod
    def listar_partidas(db: Session, torneio_id: Optional[int] = None) -> List[PartidaResponse]:
        # Criar aliases para as tabelas times
        time1_alias = alias(Partida.time1.property.target, name="time1")
        time2_alias = alias(Partida.time2.property.target, name="time2")

        # Construir a query com outer joins usando aliases
        query = db.query(Partida).\
            outerjoin(time1_alias, time1_alias.c.id == Partida.time1_id).\
            outerjoin(time2_alias, time2_alias.c.id == Partida.time2_id)
        
        if torneio_id is not None:
            query = query.filter(Partida.torneio_id == torneio_id)
        
        partidas = query.all()
        return [PartidaResponse(
            id=p.id,
            time1_nome=p.time1.nome if p.time1 else f"Time {p.time1_id} (Não encontrado)",
            time2_nome=p.time2.nome if p.time2 else f"Time {p.time2_id} (Não encontrado)",
            time1_logo=p.time1.logo if p.time1 else None,
            time2_logo=p.time2.logo if p.time2 else None,
            data=p.data,
            resultado=p.resultado
        ) for p in partidas]

    @staticmethod
    def obter_partida(db: Session, partida_id: int) -> PartidaResponse:
        # Usar aliases também aqui
        time1_alias = alias(Partida.time1.property.target, name="time1")
        time2_alias = alias(Partida.time2.property.target, name="time2")

        partida = db.query(Partida).\
            outerjoin(time1_alias, time1_alias.c.id == Partida.time1_id).\
            outerjoin(time2_alias, time2_alias.c.id == Partida.time2_id).\
            filter(Partida.id == partida_id).first()
        
        if not partida:
            return None
        return PartidaResponse(
            id=partida.id,
            time1_nome=partida.time1.nome if partida.time1 else "Desconhecido",
            time2_nome=partida.time2.nome if partida.time2 else "Desconhecido",
            time1_logo=partida.time1.logo if partida.time1 else None,
            time2_logo=partida.time2.logo if partida.time2 else None,
            data=partida.data,
            resultado=partida.resultado
        )

    @staticmethod
    def atualizar_partida(db: Session, partida_id: int, partida: PartidaUpdate) -> PartidaResponse:
        db_partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not db_partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        for key, value in partida.dict().items():
            setattr(db_partida, key, value)
        db.commit()
        db.refresh(db_partida)
        return PartidaResponse(
            id=db_partida.id,
            time1_nome=db_partida.time1.nome if db_partida.time1 else "Desconhecido",
            time2_nome=db_partida.time2.nome if db_partida.time2 else "Desconhecido",
            time1_logo=db_partida.time1.logo if db_partida.time1 else None,
            time2_logo=db_partida.time2.logo if db_partida.time2 else None,
            data=db_partida.data,
            resultado=db_partida.resultado
        )

    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        db_partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not db_partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        db.delete(db_partida)
        db.commit()