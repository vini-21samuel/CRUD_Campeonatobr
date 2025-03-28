from sqlalchemy.orm import Session
from app.models.models import Torneio

class TorneioRepository:
    @staticmethod
    def listar_torneios(db: Session):
        return db.query(Torneio).all()

    @staticmethod
    def buscar_por_id(db: Session, torneio_id: int):
        return db.query(Torneio).filter(Torneio.id == torneio_id).first()

    @staticmethod
    def criar_torneio(db: Session, torneio: Torneio):
        db.add(torneio)
        db.commit()
        db.refresh(torneio)
        return torneio

    @staticmethod
    def atualizar_torneio(db: Session, torneio_id: int, dados: dict):
        torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
        if not torneio:
            return None  # Retorna None se não encontrou o torneio

        for key, value in dados.items():
            setattr(torneio, key, value)

        db.commit()
        db.refresh(torneio)
        return torneio

    @staticmethod
    def deletar_torneio(db: Session, torneio: Torneio):
        db.delete(torneio)
        db.commit()
