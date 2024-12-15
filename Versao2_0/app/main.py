from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.routes.jogadores import router as jogadores_router
from app.routes.partidas import router as partidas_router
from app.routes.times import router as times_router
from app import  models, schemas

# Criar todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota simples para testar se o servidor está rodando
@app.get("/")
def root():
    return {"message": "API está rodando!"}

# Incluir routers de outras rotas
app.include_router(jogadores_router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(times_router, prefix="/times", tags=["Times"])
app.include_router(partidas_router, prefix="/partidas", tags=["Partidas"])
