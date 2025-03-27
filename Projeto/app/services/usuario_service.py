from sqlalchemy.orm import Session
from app.repositories.usuario_repository import get_usuario, create_usuario, get_usuarios
from app.schemas import UsuarioCreate

def cadastrar_usuario(db: Session, usuario: UsuarioCreate):
    return create_usuario(db, usuario)

def listar_usuarios(db: Session):
    return get_usuarios(db)
