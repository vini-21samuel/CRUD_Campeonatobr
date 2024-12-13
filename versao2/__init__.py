# Exemplo de __init__.py com funções ou variáveis
from .database import SessionLocal, engine
from .models import Time, Jogador

__all__ = ['SessionLocal', 'engine', 'Time', 'Jogador']
