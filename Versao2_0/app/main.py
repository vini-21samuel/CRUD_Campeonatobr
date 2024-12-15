from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine  # Ajuste no caminho de importação
from app.routes import jogadores, times, partidas  # Ajuste no caminho de importação

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI()

# Configuração de CORS
origins = [
    "http://localhost:3000",  # Substitua pelo endereço do seu frontend, se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas no app principal
app.include_router(jogadores.router, tags=["Jogadores"], prefix="/jogadores")
app.include_router(times.router, tags=["Times"], prefix="/times")
app.include_router(partidas.router, tags=["Partidas"], prefix="/partidas")

# Rota de verificação de saúde
@app.get("/")
def health_check():
    return {"message": "API Interclasse está funcionando corretamente!"}
