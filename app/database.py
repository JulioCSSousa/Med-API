from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URI = 'mysql://root:159753@localhost:3306/pymeddb'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass