from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ContactCreate, ContactRead, LeadRead
from ..crud import create_contact, get_contacts, get_leads

router = APIRouter()

@router.post("/contacts/", response_model=ContactRead)
def api_create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db=db, contact=contact)

@router.get("/contacts/", response_model=list[ContactRead])
def api_read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_contacts(db, skip=skip, limit=limit)

@router.get("/leads/", response_model=list[LeadRead])
def api_read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_leads(db, skip=skip, limit=limit)
