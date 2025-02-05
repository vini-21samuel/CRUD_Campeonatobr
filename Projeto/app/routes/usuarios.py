from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi.templating import Jinja2Templates
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioLogin
from app import models
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

# Configuração do Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota HTML: Formulário de Registro
@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Rota HTML: Registrar Usuário
@router.post("/register", response_class=HTMLResponse)
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    user_data = UsuarioCreate(username=username, email=email, password=password)
    
    existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = Usuario(
        name=name,
        username=user_data.username,
        phone=phone,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RedirectResponse(url="/usuarios/login", status_code=303)

# Rota HTML: Formulário de Login
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Rota HTML: Login
@router.post("/login", response_class=HTMLResponse)
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    login_data = UsuarioLogin(username=email, password=password)
    
    user = db.query(models.Usuario).filter(models.Usuario.email == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/", status_code=303)  # Redireciona para a raiz após login
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/redefinir-senha", response_class=HTMLResponse)
async def redefinir_senha_form(request: Request):
    return templates.TemplateResponse("redefinir_senha.html", {"request": request})

# Rota para Redefinir Senha
@router.put("/redefinir-senha", response_class=RedirectResponse)
async def redefinir_senha(
    email: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    db: Session = Depends(get_db),
):
    # Verifica se o e-mail existe no banco de dados
    user = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="E-mail não encontrado")
    
    # Verifica se as senhas coincidem
    if nova_senha != confirmar_senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não coincidem")
    
    # Atualiza a senha no banco de dados
    user.hashed_password = get_password_hash(nova_senha)  # Lógica para criptografar a senha
    db.commit()
    db.refresh(user)
    
    # Redireciona para a tela de login após redefinir a senha
    return RedirectResponse(url="/usuarios/login", status_code=303)
