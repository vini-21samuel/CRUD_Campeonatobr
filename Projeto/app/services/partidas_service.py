from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.partida import Partida
from app.repositories.partida_repository import PartidaRepository
from app.models.time import Time
from app.schemas.partida import PartidaCreate, PartidaResponse, PartidaUpdate

class PartidaService:

    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate) -> PartidaResponse:
        nova_partida = PartidaRepository.criar_partida(db, partida)

        time1 = db.query(Time).filter(Time.id == nova_partida.time1_id).first()
        time2 = db.query(Time).filter(Time.id == nova_partida.time2_id).first()

        return PartidaResponse(
            id=nova_partida.id,
            time1_nome=time1.nome if time1 else "Desconhecido",
            time2_nome=time2.nome if time2 else "Desconhecido",
            time1_logo=time1.logo if time1 else None,
            time2_logo=time2.logo if time2 else None,
            data=nova_partida.data.strftime("%Y-%m-%d"),
            resultado=nova_partida.resultado,
        )

    @staticmethod
    def listar_partidas(db: Session):
        partidas = PartidaRepository.listar_partidas(db)
        return [
            PartidaResponse(
                id=p.id,
                time1_nome=p.time1_nome,
                time2_nome=p.time2_nome,
                time1_logo=p.time1_logo,
                time2_logo=p.time2_logo,
                data=p.data.strftime("%Y-%m-%d"),
                resultado=p.resultado
            )
            for p in partidas
        ]

    @staticmethod
    def obter_partida(db: Session, partida_id: int) -> PartidaResponse:
        partida = PartidaRepository.obter_partida(db, partida_id)
        if not partida:
            return None

        return PartidaResponse(
            id=partida.id,
            time1_nome=partida.time1_nome,
            time1_logo=partida.time1_logo,
            time2_nome=partida.time2_nome,
            time2_logo=partida.time2_logo,
            data=partida.data.strftime("%Y-%m-%d"),
            resultado=partida.resultado
        )
    
    @staticmethod
    def atualizar_partida(db: Session, partida_id: int, partida_update: PartidaUpdate):
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
    
        partida.time1_id = partida_update.time1_id
        partida.time2_id = partida_update.time2_id
        partida.data = partida_update.data
        partida.resultado = partida_update.resultado
    
        db.commit()
        db.refresh(partida)
        return partida
    
    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        PartidaRepository.deletar_partida(db, partida_id)
