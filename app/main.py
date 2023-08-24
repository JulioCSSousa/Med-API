from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from app.crud import *
from sqlalchemy.orm import Session
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=list[UserSchema])
def get_users(skip=0, limit=1000, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{id}", response_model=UserSchema)
def get_user_by_id(db: Session = Depends(get_db), id=str):
    db_user = get_user_by_id(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=User.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/patients", response_model=list[PatientSchema])
def get_patients(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    patients = get_patients(db, skip=skip, limit=limit)
    return patients
