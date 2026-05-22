from enum import auto
from typing import Any
from typing_extensions import Self

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.config import settings

# Establecemos conexión con la base de datos
engine = create_engine(settings.DATABASE_URL)

# Generador de sesión
SessionLocal = sessionmaker(
   autoflush=False,
   bind=engine
)

# Función de inicialización para operaciones SQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ExplicitDatabaseConnection:
    instance = None
    initialized = False

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if self.initialized:
            return

        SessionLocal = sessionmaker(bind=engine, autoflush=False)
        self.db = SessionLocal()

        self.initialized = True
