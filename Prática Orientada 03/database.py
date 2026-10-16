from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///biblioteca.db")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
