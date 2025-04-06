from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.partida import PartidaCreate, PartidaResponse, PartidaUpdate
from app.repositories.partida_repository import PartidaRepository
from fastapi import HTTPException

class PartidaService:
    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate) -> PartidaResponse:
        return PartidaRepository.criar_partida(db, partida)

    @staticmethod
    def listar_partidas(db: Session, torneio_id: Optional[int] = None) -> List[PartidaResponse]:
        return PartidaRepository.listar_partidas(db, torneio_id)

    @staticmethod
    def obter_partida(db: Session, partida_id: int) -> PartidaResponse:
        partida = PartidaRepository.obter_partida(db, partida_id)
        if not partida:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        return partida

    @staticmethod
    def atualizar_partida(db: Session, partida_id: int, partida: PartidaUpdate) -> PartidaResponse:
        return PartidaRepository.atualizar_partida(db, partida_id, partida)

    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        PartidaRepository.deletar_partida(db, partida_id)