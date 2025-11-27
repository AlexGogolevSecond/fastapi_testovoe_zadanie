from fastapi import FastAPI
from .routers import operators, sources, contacts
from . import models
from .database import engine

app = FastAPI(title='MiniCRM')

models.Base.metadata.create_all(bind=engine)

app.include_router(operators.router, prefix="/api/v1", tags=["operators"])
app.include_router(sources.router, prefix="/api/v1", tags=["sources"])
app.include_router(contacts.router, prefix="/api/v1", tags=["contacts"])

@app.get("/")
def read_root():
    return {"message": "Mini-CRM API"}
