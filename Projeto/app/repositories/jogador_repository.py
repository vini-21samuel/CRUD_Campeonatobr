from sqlalchemy.orm import Session
from app.models.models import Jogador
from app.schemas.schemas import JogadorCreate

class JogadorRepository:
    @staticmethod
    def criar_jogador(db: Session, jogador: JogadorCreate):
        novo_jogador = Jogador(
            id=jogador.id,
            nome=jogador.nome,
            posicao=jogador.posicao,
            gols=jogador.gols,
            time_id=jogador.time_id
        )
        db.add(novo_jogador)
        db.commit()
        db.refresh(novo_jogador)
        return novo_jogador

    @staticmethod
    def listar_jogadores(db: Session):
        return db.query(Jogador).all()

    @staticmethod
    def obter_jogador(db: Session, jogador_id: int):
        return db.query(Jogador).filter(Jogador.id == jogador_id).first()

    @staticmethod
    def atualizar_jogador(db: Session, jogador_id: int, jogador_data: JogadorCreate):
        jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
        if jogador:
            jogador.nome = jogador_data.nome
            jogador.posicao = jogador_data.posicao
            jogador.gols = jogador_data.gols
            jogador.time_id = jogador_data.time_id
            db.commit()
            db.refresh(jogador)
        return jogador

    @staticmethod
    def deletar_jogador(db: Session, jogador_id: int):
        jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
        if jogador:
            db.delete(jogador)
            db.commit()
