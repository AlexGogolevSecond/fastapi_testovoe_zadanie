from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Operator(Base):
    """Операторы"""
    __tablename__ = 'operators'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    max_load = Column(Integer, default=10)

    operator_sources = relationship("OperatorSource", back_populates="operator")
    contacts = relationship("Contact", back_populates="operator")

class Source(Base):
    """Источники"""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    operator_sources = relationship("OperatorSource", back_populates="source")
    contacts = relationship("Contact", back_populates="source")

class Lead(Base):
    """Лиды"""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)  # уникальный идентификатор лида

    contacts = relationship("Contact", back_populates="lead")

class OperatorSource(Base):
    """Вес источников для операторов"""
    __tablename__ = "operator_sources"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    weight = Column(Integer, default=1)  # ?

    operator = relationship("Operator", back_populates="operator_sources")
    source = relationship("Source", back_populates="operator_sources")

class Contact(Base):
    """Обращения/контакты"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")
