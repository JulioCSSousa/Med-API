from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from app.crud import *
from sqlalchemy.orm import Session
from app.database import Base
from sqlalchemy import select
Base.metadata.create_all(bind=engine)

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#Routes
@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@app.get("/users/", response_model=list[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

