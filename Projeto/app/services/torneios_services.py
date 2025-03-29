import os
import shutil
from sqlalchemy.orm import Session
from app.models.models import Torneio
from app.schemas.schemas import TorneioCreate

UPLOAD_DIR = "app/templates/static/imagens/torneios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TorneioService:

    @staticmethod
    def salvar_imagem_torneio(capa):
        """Salva a imagem no diretório e retorna o nome do arquivo."""
        if not capa:
            return None

        caminho_arquivo = os.path.join(UPLOAD_DIR, capa.filename)
        with open(caminho_arquivo, "wb") as buffer:
            shutil.copyfileobj(capa.file, buffer)
        
        return capa.filename

    @staticmethod
    def criar_torneio(db: Session, nome: str, organizador: str, data_inicio: str, descricao: str, formato: str, capa):
        """Cria um novo torneio e salva no banco de dados."""
        nome_capa = TorneioService.salvar_imagem_torneio(capa)

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

    @staticmethod
    def listar_torneios(db: Session):
        """Lista todos os torneios cadastrados no banco."""
        return db.query(Torneio).all()

    @staticmethod
    def editar_torneio(db: Session, torneio_id: int, nome: str, organizador: str, data_inicio: str, descricao: str, formato: str, capa):
        """Edita um torneio existente."""
        torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
        if not torneio:
            raise ValueError("Torneio não encontrado.")

        # Atualiza os dados apenas se forem fornecidos
        if nome: torneio.nome = nome
        if organizador: torneio.organizador = organizador
        if data_inicio: torneio.data_inicio = data_inicio
        if descricao: torneio.descricao = descricao
        if formato: torneio.formato = formato

        # Atualiza a capa, se uma nova for enviada
        if capa:
            nome_capa = TorneioService.salvar_imagem_torneio(capa)
            torneio.capa = nome_capa

        db.commit()
        db.refresh(torneio)
        return torneio

    @staticmethod
    def deletar_torneio(db: Session, torneio_id: int):
        """Deleta um torneio pelo ID."""
        torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
        if not torneio:
            raise ValueError("Torneio não encontrado.")

        db.delete(torneio)
        db.commit()
