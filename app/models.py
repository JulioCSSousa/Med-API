from app.database import *
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date, SmallInteger
from sqlalchemy.orm import relationship

import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    id = Column(String, name='id', primary_key=True,  default=generate_uuid())
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(String, primary_key=True, default=generate_uuid)
    patient_name = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    notes = Column(Text, default=None)
    is_active = Column(Boolean, default=True)

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(String, primary_key=True, default=generate_uuid)
    med_name = Column(String, nullable=False)
    quant_capsule_box = Column(Integer, nullable=False)

class Med_adm(Base):
    __tablename__ = 'med_adm'
    id = Column(String, primary_key=True, default=generate_uuid)
    id_patient = Column(String, ForeignKey('patients.id'))
    id_med = Column(String, ForeignKey('medicines.id'))
    quant_capsule_day = Column(SmallInteger)
    receipt_date = Column(Date)
    entry_quant = Column(Integer)
    loss = Column(Integer, default=0)
    expiration_date = Column(Date)
patients = relationship('Patient', back_populates='med_adm_patients')
medicines = relationship('Medicine', back_populates='med_adm_medicines')