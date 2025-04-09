from sqlalchemy.orm import Session
from app.models.torneio import Torneio
from app.schemas.torneio import TorneioCreate

class TorneiosRepository:

    @staticmethod
    def criar_torneio(db: Session, torneio: TorneioCreate, capa: str | None = None):
        """Cria um novo torneio e salva no banco de dados."""
        novo_torneio = Torneio(
            nome=torneio.nome,
            organizador=torneio.organizador,
            data_inicio=torneio.data_inicio,
            descricao=torneio.descricao,
            formato=torneio.formato,
            capa=capa
        )
        db.add(novo_torneio)
        db.commit()
        db.refresh(novo_torneio)
        return novo_torneio

    @staticmethod
    def listar_torneios(db: Session):
        """Retorna todos os torneios cadastrados."""
        return db.query(Torneio).all()

    @staticmethod
    def buscar_torneio_por_id(db: Session, torneio_id: int):
        """Busca um torneio pelo ID."""
        return db.query(Torneio).filter(Torneio.id == torneio_id).first()

    @staticmethod
    def atualizar_torneio(db: Session, torneio_id: int, torneio: TorneioCreate, capa: str | None = None):
        """Atualiza um torneio existente no banco de dados."""
        torneio_atual = db.query(Torneio).filter(Torneio.id == torneio_id).first()
        if not torneio_atual:
            return None

        torneio_atual.nome = torneio.nome
        torneio_atual.organizador = torneio.organizador
        torneio_atual.data_inicio = torneio.data_inicio
        torneio_atual.descricao = torneio.descricao
        torneio_atual.formato = torneio.formato
        if capa:
            torneio_atual.capa = capa

        db.commit()
        db.refresh(torneio_atual)
        return torneio_atual

    @staticmethod
    def deletar_torneio(db: Session, torneio_id: int):
        """Deleta um torneio pelo ID."""
        torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
        if not torneio:
            return None
        db.delete(torneio)
        db.commit()
