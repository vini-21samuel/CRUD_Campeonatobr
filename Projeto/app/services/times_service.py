from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app.repositories.time_repository import TimeRepository
from app.schemas.schemas import TimeCreate, TimeResponse
import os
import shutil

UPLOAD_DIR_TIMES = "app/templates/static/imagens/times"
os.makedirs(UPLOAD_DIR_TIMES, exist_ok=True, mode=0o775)

class TimeService:
    @staticmethod
    def salvar_imagem_time(logo: UploadFile) -> str:
        if not logo:
            return None
        caminho_arquivo = os.path.join(UPLOAD_DIR_TIMES, logo.filename)
        with open(caminho_arquivo, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)
        return logo.filename

    @staticmethod
    def criar_time(db: Session, time: TimeCreate, logo: UploadFile = None):
        nome_logo = TimeService.salvar_imagem_time(logo) if logo else None
        return TimeRepository.criar_time(db, time, nome_logo)

    @staticmethod
    def listar_times(db: Session):
        return TimeRepository.listar_times(db)

    @staticmethod
    def listar_times_por_torneio(db: Session, torneio_id: int):
        return TimeRepository.listar_times_por_torneio(db, torneio_id)

    @staticmethod
    def obter_time(db: Session, time_id: int):
        time = TimeRepository.obter_time(db, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return time

    @staticmethod
    def atualizar_time(db: Session, time_id: int, time_data: TimeCreate, logo: UploadFile = None):
        time = TimeRepository.obter_time(db, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        nome_logo = TimeService.salvar_imagem_time(logo) if logo else time.logo
        return TimeRepository.atualizar_time(db, time_id, time_data, nome_logo)

    @staticmethod
    def deletar_time(db: Session, time_id: int):
        time = TimeRepository.obter_time(db, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        TimeRepository.deletar_time(db, time_id)
        return {"detail": "Time deletado com sucesso"}