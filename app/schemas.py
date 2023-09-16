from pydantic import BaseModel


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
    patient_name: str or None=None
    notes: str or None=None

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
    med_name: str
    quant_capsule_box: int
    quant_capsule_day: int
    receipt_date: str
    entry_quant: int
    loss: int
    expiration_date: str

class MedAdmCreate(MedAdmBase):
    pass

class MedAdmSchema(MedAdmBase):
    id: str
    id_patient: list[PatientSchema] = []
    id_med: list[MedicineSchema] = []

    class Config:
        orm_mode = True
