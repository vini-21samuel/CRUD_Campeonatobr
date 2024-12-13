from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from versao2.database import get_db
from versao2 import models, schemas

router = APIRouter()

# Rotas para Times
@router.get("/times", response_model=list[schemas.TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    return db.query(models.Time).all()

@router.post("/times", response_model=schemas.TimeResponse)
def criar_time(time: schemas.TimeCreate, db: Session = Depends(get_db)):
    novo_time = models.Time(nome=time.nome, lugar=time.lugar)
    db.add(novo_time)
    db.commit()
    db.refresh(novo_time)
    return novo_time

@router.put("/times/{time_id}", response_model=schemas.TimeResponse)
def atualizar_time(time_id: int, time: schemas.TimeCreate, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not db_time:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    db_time.nome = time.nome
    db_time.lugar = time.lugar
    db.commit()
    db.refresh(db_time)
    return db_time

@router.delete("/times/{time_id}")
def deletar_time(time_id: int, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not db_time:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    db.delete(db_time)
    db.commit()
    return {"mensagem": "Time deletado com sucesso."}

# Rotas para Jogadores
@router.get("/jogadores", response_model=list[schemas.JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    return db.query(models.Jogador).all()

@router.post("/jogadores", response_model=schemas.JogadorResponse)
def criar_jogador(jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    novo_jogador = models.Jogador(
        nome=jogador.nome, 
        posicao=jogador.posicao, 
        gols=jogador.gols, 
        time_id=jogador.time_id
    )
    db.add(novo_jogador)
    db.commit()
    db.refresh(novo_jogador)
    return novo_jogador

@router.put("/jogadores/{jogador_id}", response_model=schemas.JogadorResponse)
def atualizar_jogador(jogador_id: int, jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not db_jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
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
    if not db_jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
    db.delete(db_jogador)
    db.commit()
    return {"mensagem": "Jogador deletado com sucesso."}

# Rotas para Partidas
@router.get("/partidas", response_model=list[schemas.PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return db.query(models.Partida).all()

@router.post("/partidas", response_model=schemas.PartidaResponse)
def criar_partida(partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    nova_partida = models.Partida(
        time_casa_id=partida.time_casa_id,
        time_visitante_id=partida.time_visitante_id,
        data=partida.data,
        placar=partida.placar
    )
    db.add(nova_partida)
    db.commit()
    db.refresh(nova_partida)
    return nova_partida

@router.put("/partidas/{partida_id}", response_model=schemas.PartidaResponse)
def atualizar_partida(partida_id: int, partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not db_partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    db_partida.time_casa_id = partida.time_casa_id
    db_partida.time_visitante_id = partida.time_visitante_id
    db_partida.data = partida.data
    db_partida.placar = partida.placar
    db.commit()
    db.refresh(db_partida)
    return db_partida

@router.delete("/partidas/{partida_id}")
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not db_partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    db.delete(db_partida)
    db.commit()
    return {"mensagem": "Partida deletada com sucesso."}
