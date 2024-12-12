from App.database import SessionLocal
from App.models import Time
from App.schemas import TimeCreate, TimeResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TimeResponse, tags=["Times"])
def criar_time(time: TimeCreate, db: Session = Depends(get_db)):
    novo_time = Time(nome=time.nome, lugar=time.lugar)
    db.add(novo_time)
    db.commit()
    db.refresh(novo_time)
    return novo_time
