from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URI = 'mysql://root:hFD4eh1F6CaH2abFaBeCh3h2D4-2Bh-g@monorail.proxy.rlwy.net:49181/railway'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass