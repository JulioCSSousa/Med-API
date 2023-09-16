from fastapi import FastAPI
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from app.auth_user import *
from app.crud import *
from sqlalchemy.orm import Session
from app.database import Base
Base.metadata.create_all(bind=engine)
from fastapi.responses import JSONResponse
db = Session(engine)

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




@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate":"Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    access_token = create_access_token(data={"sub": user}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type":"bearer"}

@app.post("/users/", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = generate_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse (content=f"{user.nome, user.email} Cadastrado com sucesso")

@app.get("/users/me", response_model=TokenData)
def read_user_me(current_user: TokenData = Depends(get_current_user)):
    return current_user

@app.get("/users/", response_model=list[UserSchema])
def read_users(skip: int = 0, limit: int = 100, TokenData = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(id: str, TokenData = Depends(get_current_user)):
    db_user = get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@app.get("/patients/", response_model=list[PatientSchema])
def read_patients(skip: int = 0, limit: int = 100, TokenData = Depends(get_current_user)):
    patients = get_patients(db, skip=skip, limit=limit)
    return patients

@app.get("/patients/{id}", response_model=PatientSchema)
def read_patient_id(id: str, TokenData = Depends(get_current_user)):
    patient = get_patient(db, id=id)
    if not patient.is_active:
        raise HTTPException(status_code=404, detail=f"seems {patient.patient_name} is a inactive patient")
    return patient

@app.post("/patients/", response_model=PatientCreate)
def new_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = get_patient_by_cpf(db, cpf=patient.cpf)
    if db_patient:
        raise HTTPException(status_code=400, detail="CPF already registered")
    db_patient = Patient(patient_name=patient.patient_name, cpf=patient.cpf, notes=patient.notes, is_active=True)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return JSONResponse(f"{db_patient.patient_name}  Cadastradoc com sucesso")

@app.get("/medicines/", response_model=list[MedicineSchema])
def read_medicines(skip: int = 0, limit: int = 100, TokenData = Depends(get_current_user)):
    medicines = get_medicines(db, skip=skip, limit=limit)
    return medicines

@app.get("/medicines/{id}", response_model=MedicineSchema)
def read_medicine_id(id: str, TokenData = Depends(get_current_user)):
    medicine = get_medicine(db, id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@app.post("/medicines/", response_model=MedicineCreate)
def new_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):

    db_medicine = Medicine(med_name=medicine.med_name, quant_capsule_box=medicine.quant_capsule_box)
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return JSONResponse(f"{db_medicine.med_name}  Cadastradoc com sucesso")

@app.get("/med_adm/", response_model=list[MedAdmSchema])
def get_med_adm(skip: int = 0, limit: int = 100, TokenData = Depends(get_current_user)):
    med_adm = get_admistration(db, skip=skip, limit=limit)
    return med_adm