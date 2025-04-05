from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.jogador import Jogador
from app.repositories.jogador_repository import JogadorRepository
from app.schemas.jogador import JogadorCreate
from sqlalchemy.orm import joinedload

class JogadorService:
    @staticmethod
    def criar_jogador(db: Session, jogador: JogadorCreate):
        return JogadorRepository.criar_jogador(db, jogador)

    @staticmethod
    def listar_jogadores(db: Session):
        return db.query(Jogador).options(joinedload(Jogador.time)).all()

    @staticmethod
    def obter_jogador(db: Session, jogador_id: int):
        jogador = JogadorRepository.obter_jogador(db, jogador_id)
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        return jogador

    @staticmethod
    def atualizar_jogador(db: Session, jogador_id: int, jogador_data: JogadorCreate):
        jogador = JogadorRepository.atualizar_jogador(db, jogador_id, jogador_data)
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado para atualizar")
        return jogador

    @staticmethod
    def deletar_jogador(db: Session, jogador_id: int):
        jogador = JogadorRepository.obter_jogador(db, jogador_id)
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado para deletar")
        JogadorRepository.deletar_jogador(db, jogador_id)
