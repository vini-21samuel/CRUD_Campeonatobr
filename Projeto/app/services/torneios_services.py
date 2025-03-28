from sqlalchemy.orm import Session
from app.models.models import Torneio
import os
import shutil
from datetime import datetime

UPLOAD_DIR = "app/templates/static/imagens/torneios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TorneioService:
    @staticmethod
    def listar_torneios(db: Session):
        return db.query(Torneio).all()

    @staticmethod
    def criar_torneio(db: Session, nome: str, organizador: str, data_inicio: str, descricao: str, formato: str, capa):
        try:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()

            if db.query(Torneio).filter(Torneio.nome == nome).first():
                raise ValueError("Torneio com esse nome já existe.")

            nome_capa = None
            if capa:
                nome_capa = f"{datetime.now().timestamp()}_{capa.filename}"
                caminho_capa = os.path.join(UPLOAD_DIR, nome_capa)
                with open(caminho_capa, "wb") as buffer:
                    shutil.copyfileobj(capa.file, buffer)

            novo_torneio = Torneio(
                nome=nome,
                organizador=organizador,
                data_inicio=data_inicio,
                descricao=descricao,
                formato=formato,
                capa=nome_capa
            )

            db.add(novo_torneio)
            db.commit()
            db.refresh(novo_torneio)
            return novo_torneio

        except ValueError as e:
            db.rollback()
            raise ValueError(str(e))
        except Exception as e:
            db.rollback()
            print(f"Erro ao criar torneio: {e}")
            raise ValueError("Erro interno ao criar torneio.")

    @staticmethod
    def editar_torneio(db: Session, torneio_id: int, nome: str = None, organizador: str = None, data_inicio: str = None, descricao: str = None, formato: str = None, capa=None):
        torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
        if not torneio:
            raise ValueError("Torneio não encontrado.")

        if nome:
            torneio.nome = nome
        if organizador:
            torneio.organizador = organizador
        if data_inicio:
            torneio.data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        if descricao:
            torneio.descricao = descricao
        if formato:
            torneio.formato = formato
        if capa:
            if torneio.capa:
                caminho_antigo = os.path.join(UPLOAD_DIR, torneio.capa)
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)

            nome_capa = f"{datetime.now().timestamp()}_{capa.filename}"
            caminho_capa = os.path.join(UPLOAD_DIR, nome_capa)
            with open(caminho_capa, "wb") as buffer:
                shutil.copyfileobj(capa.file, buffer)

            torneio.capa = nome_capa

        db.commit()
        db.refresh(torneio)
        return torneio
