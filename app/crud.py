from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app.models import *
from app.schemas import *


def get_user(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str, skip: int = 0, limit: int = 100):
    return db.query(User.email).filter(User.email == email).offset(skip).limit(limit).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def createUser(db: Session, user: UserCreate):
    hashed_password = generate_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def get_patient(db: Session, id: str):
    return db.query(Patient).filter(Patient.id == id).first()



def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(name=patient.patient_name, cpf=patient.cpf, notes=patient.notes)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_medicine(db: Session, id: str):
    return db.query(Medicine).filter(Medicine.id == id).first()


def get_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()


def create_medicine(db: Session, medicine: MedicineCreate):
    db_medicine = medicines(name=medicine.med_name, quant=medicine.quant_capsule_box)
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine
