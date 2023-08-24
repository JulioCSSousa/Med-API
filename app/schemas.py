from pydantic import BaseModel
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: str
    is_active: bool


class PatientBase(BaseModel):
    patient_name: str
    cpf: str

class PatientCreate(PatientBase):
    pass

class PatientSchema(PatientBase):
    id: str

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
