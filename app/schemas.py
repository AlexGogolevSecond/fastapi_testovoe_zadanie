from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class OperatorBase(BaseModel):
    name: str
    is_active: bool = True
    max_load: int = 10

    model_config = {"from_attributes": True}

class OperatorCreate(OperatorBase):
    pass

class OperatorRead(OperatorCreate):
    id: int

class SourceBase(BaseModel):
    name: str

    model_config = {"from_attributes": True}

class SourceCreate(SourceBase):
    pass

class SourceRead(SourceCreate):
    id: int

class LeadBase(BaseModel):
    external_id: str

    model_config = {"from_attributes": True}

class LeadCreate(LeadBase):
    pass

class LeadRead(LeadCreate):
    id: int

class OperatorSourceBase(BaseModel):
    operator_id: int
    source_id: int
    weight: int = 1

    model_config = {"from_attributes": True}

class OperatorSourceCreate(OperatorSourceBase):
    pass

class OperatorSourceRead(OperatorSourceCreate):
    id: int

class ContactBase(BaseModel):
    lead_id: int
    source_id: int
    operator_id: Optional[int] = None

    model_config = {"from_attributes": True}

class ContactCreate(BaseModel):
    external_id: str
    source_id: int

    @field_validator("external_id", mode="before")
    @classmethod
    def normalize_external_id(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

class ContactRead(ContactBase):
    id: int
    created_at: datetime
