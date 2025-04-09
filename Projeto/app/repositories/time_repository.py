from sqlalchemy.orm import Session
from app.models.time import Time
from app.schemas.time import TimeCreate

class TimeRepository:
    @staticmethod
    def criar_time(db: Session, time: TimeCreate, logo: str = None):
        db_time = Time(nome=time.nome, lugar=time.lugar, torneio_id=time.torneio_id, logo=logo)
        db.add(db_time)
        db.commit()
        db.refresh(db_time)
        return db_time

    @staticmethod
    def listar_times(db: Session):
        return db.query(Time).all()

    @staticmethod
    def listar_times_por_torneio(db: Session, torneio_id: int):
        return db.query(Time).filter(Time.torneio_id == torneio_id).all()

    @staticmethod
    def obter_time(db: Session, time_id: int):
        return db.query(Time).filter(Time.id == time_id).first()

    @staticmethod
    def atualizar_time(db: Session, time_id: int, time_data: TimeCreate, logo: str = None):
        time = db.query(Time).filter(Time.id == time_id).first()
        if time:
            time.nome = time_data.nome
            time.lugar = time_data.lugar
            time.torneio_id = time_data.torneio_id
            time.logo = logo if logo else time.logo  # Atualiza o logo apenas se fornecido
            db.commit()
            db.refresh(time)
        return time

    @staticmethod
    def deletar_time(db: Session, time_id: int):
        time = db.query(Time).filter(Time.id == time_id).first()
        if time:
            db.delete(time)
            db.commit()