from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .rotas import time, jogador, partida

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(time.router, prefix="/times", tags=["Times"])
app.include_router(jogador.router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(partida.router, prefix="/partidas", tags=["Partidas"])

@app.get("/api/healthchecker")
def health_check():
    return {"message": "API Interclasse está funcionando!"}
