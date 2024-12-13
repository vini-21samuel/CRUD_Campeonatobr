from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from versao2_0.database import engine
from versao2_0 import models
from .rotas import note

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

app.include_router(note.router, prefix="/api", tags=["Times, Jogadores, Partidas"])

@app.get("/api/healthchecker")
def health_check():
    return {"message": "API Interclasse está funcionando!"}
