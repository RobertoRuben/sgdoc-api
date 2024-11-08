from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(
    title="SGDOC API",
    description="API para el sistema de gestión de documentos",
    version="0.1.0",
    debug=True,
    lifespan=lifespan
)
