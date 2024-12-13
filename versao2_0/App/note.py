from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ... import models, schemas
from typing import List

# Função para obter o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------- CRUD para Times -------------

router = APIRouter()

@router.post("/times/", response_model=schemas.TimeResponse)
def criar_time(time: schemas.TimeCreate, db: Session = Depends(get_db)):
    db_time = models.Time(nome=time.nome, lugar=time.lugar)
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time

@router.get("/times/", response_model=List[schemas.TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    return db.query(models.Time).all()

@router.get("/times/{time_id}", response_model=schemas.TimeResponse)
def obter_time(time_id: int, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if db_time is None:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return db_time

@router.put("/times/{time_id}", response_model=schemas.TimeResponse)
def atualizar_time(time_id: int, time: schemas.TimeCreate, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if db_time is None:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    db_time.nome = time.nome
    db_time.lugar = time.lugar
    db.commit()
    db.refresh(db_time)
    return db_time

@router.delete("/times/{time_id}")
def deletar_time(time_id: int, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if db_time is None:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    db.delete(db_time)
    db.commit()
    return {"message": "Time deletado com sucesso"}

# ------------- CRUD para Jogadores -------------

@router.post("/jogadores/", response_model=schemas.JogadorResponse)
def criar_jogador(jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    db_jogador = models.Jogador(**jogador.dict())
    db.add(db_jogador)
    db.commit()
    db.refresh(db_jogador)
    return db_jogador

@router.get("/jogadores/", response_model=List[schemas.JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    return db.query(models.Jogador).all()

@router.get("/jogadores/{jogador_id}", response_model=schemas.JogadorResponse)
def obter_jogador(jogador_id: int, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if db_jogador is None:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return db_jogador

@router.put("/jogadores/{jogador_id}", response_model=schemas.JogadorResponse)
def atualizar_jogador(jogador_id: int, jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if db_jogador is None:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    db_jogador.nome = jogador.nome
    db_jogador.posicao = jogador.posicao
    db_jogador.gols = jogador.gols
    db_jogador.time_id = jogador.time_id
    db.commit()
    db.refresh(db_jogador)
    return db_jogador

@router.delete("/jogadores/{jogador_id}")
def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if db_jogador is None:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    db.delete(db_jogador)
    db.commit()
    return {"message": "Jogador deletado com sucesso"}

# ------------- CRUD para Partidas -------------

@router.post("/partidas/", response_model=schemas.PartidaResponse)
def criar_partida(partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    db_partida = models.Partida(**partida.dict())
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida

@router.get("/partidas/", response_model=List[schemas.PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return db.query(models.Partida).all()

@router.get("/partidas/{partida_id}", response_model=schemas.PartidaResponse)
def obter_partida(partida_id: int, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if db_partida is None:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return db_partida

@router.put("/partidas/{partida_id}", response_model=schemas.PartidaResponse)
def atualizar_partida(partida_id: int, partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if db_partida is None:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    db_partida.data = partida.data
    db_partida.gols_time1 = partida.gols_time1
    db_partida.gols_time2 = partida.gols_time2
    db_partida.time1_id = partida.time1_id
    db_partida.time2_id = partida.time2_id
    db.commit()
    db.refresh(db_partida)
    return db_partida

@router.delete("/partidas/{partida_id}")
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if db_partida is None:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    db.delete(db_partida)
    db.commit()
    return {"message": "Partida deletada com sucesso"}
