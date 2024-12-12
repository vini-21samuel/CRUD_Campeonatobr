from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from schemas import TimeCreate, JogadorCreate, TimeResponse, JogadorResponse
from Rotas.time import app as time_router
from Rotas.jogadores import app as jogadores_router

# criar as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(time_router, prefix="/times", tags=["Times"])
app.include_router(jogadores_router, prefix="/jogadores", tags=["Jogadores"])

# essas são as dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# rotas para Times
@app.get("/times/", response_model=list[TimeResponse], tags=["Times"])
def listar_times(db: Session = Depends(get_db)):
    return db.query(models.Time).all()

@app.post("/times/", response_model=TimeResponse, tags=["Times"])
def adicionar_time(time: TimeCreate, db: Session = Depends(get_db)):
    db_time = models.Time(nome=time.nome, lugar=time.lugar)
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time

@app.put("/times/{time_id}", response_model=TimeResponse, tags=["Times"])
def atualizar_time(time_id: int, time: TimeCreate, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not db_time:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    db_time.nome = time.nome
    db_time.lugar = time.lugar
    db.commit()
    db.refresh(db_time)
    return db_time

@app.delete("/times/{time_id}", tags=["Times"])
def deletar_time(time_id: int, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not db_time:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    db.delete(db_time)
    db.commit()
    return {"mensagem": "Time deletado com sucesso."}

# Rotas para Jogadores
@app.get("/jogadores/", response_model=list[JogadorResponse], tags=["Jogadores"])
def listar_jogadores(db: Session = Depends(get_db)):
    return db.query(models.Jogador).all()

@app.post("/jogadores/", response_model=JogadorResponse, tags=["Jogadores"])
def adicionar_jogador(jogador: JogadorCreate, db: Session = Depends(get_db)):
    db_jogador = models.Jogador(
        nome=jogador.nome,
        posicao=jogador.posicao,
        gols=jogador.gols,
        time_id=jogador.time_id,
    )
    db.add(db_jogador)
    db.commit()
    db.refresh(db_jogador)
    return db_jogador

@app.put("/jogadores/{jogador_id}", response_model=JogadorResponse, tags=["Jogadores"])
def atualizar_jogador(jogador_id: int, jogador: JogadorCreate, db: Session = Depends(get_db)):
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

@app.delete("/jogadores/{jogador_id}", tags=["Jogadores"])
def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not db_jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
    db.delete(db_jogador)
    db.commit()
    return {"mensagem": "Jogador deletado com sucesso."}
