from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app.models import *
from app.schemas import *


def get_user(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User.email).filter(User.email == email).first()
def get_user_pwd(db: Session, email: str):
    return db.query(User.password).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def activated(db: Session, id:str):
    active = bool(db.query(Patient.is_active).filter(Patient.id==id).first())
    return active




def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def get_patient(db: Session, id: str):
    patient = db.query(Patient).filter(Patient.id == id).first()
    return patient

def get_patient_by_cpf(db: Session, cpf: str):
    patient = db.query(Patient.cpf).filter(Patient.cpf == cpf).first()
    return patient


def get_medicine(db: Session, id: str):
    return db.query(Medicine).filter(Medicine.id == id).first()


def get_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()


def get_admistration(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Med_adm).offset(skip).limit(limit).all()