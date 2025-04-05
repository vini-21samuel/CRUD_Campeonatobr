from sqlalchemy.orm import Session, aliased
from app.models.partida import Partida
from app.models.time import Time
from app.schemas.partida import PartidaCreate

class PartidaRepository:

    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate):
        nova_partida = Partida(
            time1_id=partida.time1_id,
            time2_id=partida.time2_id,
            data=partida.data,
            resultado=partida.resultado,
        )
        db.add(nova_partida)
        db.commit()
        db.refresh(nova_partida)
        return nova_partida


    @staticmethod
    def listar_partidas(db: Session):
        Time1 = aliased(Time)
        Time2 = aliased(Time)

        return db.query(
            Partida.id,
            Partida.data,
            Partida.resultado,
            Time1.nome.label("time1_nome"),
            Time1.logo.label("time1_logo"),
            Time2.nome.label("time2_nome"),
            Time2.logo.label("time2_logo")
        ).join(Time1, Partida.time1_id == Time1.id
        ).join(Time2, Partida.time2_id == Time2.id
        ).all()


    @staticmethod
    def obter_partida(db: Session, partida_id: int):
        Time1 = aliased(Time)
        Time2 = aliased(Time)

        return db.query(
            Partida.id,
            Partida.data,
            Partida.resultado,
            Time1.nome.label("time1_nome"),
            Time1.logo.label("time1_logo"), 
            Time2.nome.label("time2_nome"),
            Time2.logo.label("time2_logo")   
        ).join(Time1, Partida.time1_id == Time1.id
        ).join(Time2, Partida.time2_id == Time2.id
        ).filter(Partida.id == partida_id).first()

    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if partida:
            db.delete(partida)
            db.commit()
