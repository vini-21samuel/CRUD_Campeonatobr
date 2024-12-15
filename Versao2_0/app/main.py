from fastapi import FastAPI
from app.database import Base, engine
from app.routers import jogador, times, partidas

# Cria as tabelas no banco de dados (apenas na inicialização do servidor)
print("Iniciando criação de tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")


app = FastAPI()

# Incluindo as rotas
app.include_router(jogador.router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(times.router, prefix="/times", tags=["Times"])
app.include_router(partidas.router, prefix="/partidas", tags=["Partidas"])

# Rota simples para testar se o servidor está rodando
@app.get("/")
def root():
    return {"message": "API está rodando!"}
