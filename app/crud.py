from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .models import Operator, Source, Lead, OperatorSource, Contact
from .schemas import OperatorCreate, SourceCreate, LeadCreate, OperatorSourceCreate, ContactCreate
import random

def get_operator(db: Session, operator_id: int):
    return db.query(Operator).filter(Operator.id == operator_id).first()

def get_operator_by_name(db: Session, name: str):
    if name is None:
        return None
    norm = name.strip().lower()
    return db.query(Operator).filter(func.lower(Operator.name) == norm).first()

def get_operators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Operator).offset(skip).limit(limit).all()

def create_operator(db: Session, operator: OperatorCreate):
    # normalize name before creating
    data = operator.model_dump()
    if "name" in data and isinstance(data["name"], str):
        data["name"] = data["name"].strip()
    db_operator = Operator(**data)
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator

def update_operator(db: Session, operator_id: int, operator: OperatorCreate):
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if db_operator:
        for key, value in operator.model_dump().items():
            setattr(db_operator, key, value)
        db.commit()
        db.refresh(db_operator)
    return db_operator

def get_source(db: Session, source_id: int):
    return db.query(Source).filter(Source.id == source_id).first()

def get_sources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Source).offset(skip).limit(limit).all()

def create_source(db: Session, source: SourceCreate):
    db_source = Source(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

def get_lead_by_external_id(db: Session, external_id: str):
    return db.query(Lead).filter(Lead.external_id == external_id).first()

def create_lead(db: Session, lead: LeadCreate):
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_operator_sources(db: Session, source_id: int):
    return db.query(OperatorSource).filter(OperatorSource.source_id == source_id).all()

def create_operator_source(db: Session, op_source: OperatorSourceCreate):
    db_op_source = OperatorSource(**op_source.model_dump())
    db.add(db_op_source)
    db.commit()
    db.refresh(db_op_source)
    return db_op_source

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lead).offset(skip).limit(limit).all()

def assign_operator(db: Session, source_id: int):
    op_sources = get_operator_sources(db, source_id)
    available_ops = []
    for op_s in op_sources:
        op = op_s.operator
        if op and op.is_active:
            current_load = db.query(Contact).filter(Contact.operator_id == op.id).count()
            if current_load < (op.max_load or 0):
                available_ops.append((op, op_s.weight))

    if not available_ops:
        return None  # нет свободных операторов

    total_weight = sum(weight for _, weight in available_ops)
    if total_weight == 0:
        return None
    rand = random.uniform(0, total_weight)
    cumulative = 0
    for op, weight in available_ops:
        cumulative += weight
        if rand <= cumulative:
            current_load = db.query(Contact).filter(Contact.operator_id == op.id).count()  # м.б. дорого
            if current_load < (op.max_load or 0):
                return op

    return None

def create_contact(db: Session, contact: ContactCreate):
    lead = get_lead_by_external_id(db, contact.external_id)
    if not lead:
        lead = create_lead(db, LeadCreate(external_id=contact.external_id))

    operator = assign_operator(db, contact.source_id)

    db_contact = Contact(lead_id=lead.id, source_id=contact.source_id, operator_id=operator.id if operator else None)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
