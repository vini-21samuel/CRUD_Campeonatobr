from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database.database import engine, Base, get_db
from app.utils.auth import decode_token
# Importe todos os modelos explicitamente
from app.models.usuario import Usuario
from app.models.torneio import Torneio
from app.models.time import Time
from app.models.partida import Partida
from app.models.jogador import Jogador

app = FastAPI()

# Cria todas as tabelas definidas nos modelos
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not decode_token(token):
        return RedirectResponse(url="/usuarios/login", status_code=303)
    torneios = db.query(Torneio).all()
    return templates.TemplateResponse("base.html", {"request": request, "torneios": torneios})


from app.routes.times import router as times_router
from app.routes.jogadores import router as jogadores_router
from app.routes.partidas import router as partidas_router
from app.routes.usuarios import router as usuarios_router
from app.routes.torneios import router as torneios_router

app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(times_router, prefix="/times", tags=["Times"])
app.include_router(jogadores_router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(partidas_router, prefix="/partidas", tags=["Partidas"])
app.include_router(torneios_router, prefix="/torneios", tags=["Torneios"])