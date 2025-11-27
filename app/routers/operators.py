from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import OperatorCreate, OperatorRead
from ..crud import create_operator, get_operators, update_operator

router = APIRouter()

@router.post("/operators/", response_model=OperatorRead)
def api_create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    return create_operator(db=db, operator=operator)

@router.get("/operators/", response_model=list[OperatorRead])
def api_read_operators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_operators(db, skip=skip, limit=limit)

@router.put("/operators/{operator_id}", response_model=OperatorRead)
def api_update_operator(operator_id: int, operator: OperatorCreate, db: Session = Depends(get_db)):
    db_operator = update_operator(db, operator_id, operator)
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator
