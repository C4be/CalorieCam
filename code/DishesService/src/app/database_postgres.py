from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

import os

host = os.environ.get("POSTGRES_HOST", "localhost")
port = os.environ.get("POSTGRES_PORT", "5432")
user = os.environ.get("POSTGRES_USER", "admin")
password = os.environ.get("POSTGRES_PASSWORD", "password")
db = os.environ.get("POSTGRES_DB", "caloriecam")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# test
# DATABASE_URL = "postgresql://admin:password@localhost:5432/caloriecam"

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()



def get_db() -> Generator[Session, None, None]:
    """
    Функция-генератор для получения сессии с базой данных.

    :return: Сессия SQLAlchemy для выполнения операций с базой данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







