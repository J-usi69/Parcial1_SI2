import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables desde .env
load_dotenv()

# PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/veltra_db"
)

# Engine configurado para PostgreSQL
engine = create_engine(DATABASE_URL)

# Sesión local para interactuar con la Base de Datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa principal
Base = declarative_base()

def get_db():
    """
    Dependencia de FastAPI para inyectar la sesión de la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()