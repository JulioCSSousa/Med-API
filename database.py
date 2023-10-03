from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URI = 'mysql://root:ZTaQxeQttlYLn77wJ6sb@containers-us-west-50.railway.app:6233/railway'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass