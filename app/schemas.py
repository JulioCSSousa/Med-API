from pydantic import BaseModel
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserSchema(UserCreate):
    id: str
    email: str

class TokenData(BaseModel):
    email: str

class PatientBase(BaseModel):
    patient_name: str
    notes: str

class PatientCreate(PatientBase):
    cpf: str

class PatientSchema(PatientBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True


class MedicineBase(BaseModel):
    med_name: str
    quant_capsule_box: int

class MedicineCreate(MedicineBase):
    pass

class MedicineSchema(MedicineBase):
    id: str

    class Config:
        orm_mode = True

class MedAdmBase(BaseModel):
    quant_capsule_day: int
    receipt_date: date
    entry_quant: int
    loss: int
    expiration_date: date

class MedAdmCreate(MedAdmBase):
    id_patient: str
    id_med: str

class MedAdmSchema(MedAdmBase):
    id: str


    class Config:
        orm_mode = True
