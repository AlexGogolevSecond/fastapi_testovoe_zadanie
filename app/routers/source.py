from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import SourceCreate, SourceRead, OperatorSourceCreate, OperatorSourceRead
from ..crud import create_source, get_sources, create_operator_source

router = APIRouter()

@router.post("/sources/", response_model=SourceRead)
def api_create_source(source: SourceCreate, db: Session = Depends(get_db)):
    return create_source(db=db, source=source)

@router.get("/sources/", response_model=list[SourceRead])
def api_read_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_sources(db, skip=skip, limit=limit)

@router.post("/operator-sources/", response_model=OperatorSourceRead)
def api_create_operator_source(op_source: OperatorSourceCreate, db: Session = Depends(get_db)):
    return create_operator_source(db=db, op_source=op_source)
