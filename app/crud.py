from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import *
from app.schemas import *
from fastapi import HTTPException
from fastapi.responses import JSONResponse
db = Session(engine)


def get_user(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

def get_user_by_username(db: Session, username: str):
    user = db.query(User.username).filter(User.username == username).first()
    return user
def get_user_pwd(db: Session, username: str):
    pwd = db.query(User.password).filter(User.username == username).first()
    print(pwd[0])
    return pwd

def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


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
    sql = """SELECT patients.id, patients.patient_name, medicines.med_name, med_adm.quant_capsule_day, receipt_date, entry_quant, loss, expiration_date
                      FROM patients
                      JOIN med_adm
                      ON patients.id = med_adm.id_patient
                      JOIN medicines
                      ON medicines.id = med_adm.id_med;"""
    with engine.connect() as conect:
        result = conect.execute(text(sql))
    lst_med_adm = []
    for adm in result:
        lst_med_adm.append({'Nome do Cliente': adm[1],
                            'Nome do Remedio': adm[2],
                            'Quantidade por Dia': adm[3],
                            'receipt_date': str(adm[4]),
                            'entry_quant': adm[5],
                            'perda': adm[6],
                            'expiration_date': str(adm[7]) })
    return JSONResponse(lst_med_adm)

def get_adminstration_by_id(db: Session, id: str):
    sql = """SELECT patients.id, patients.patient_name, medicines.med_name, med_adm.quant_capsule_day, 
    receipt_date, entry_quant, loss, expiration_date, patients.is_active
                      FROM patients
                      JOIN med_adm
                      ON patients.id = med_adm.id_patient
                      JOIN medicines
                      ON medicines.id = med_adm.id_med;"""
    with engine.connect() as conect:
        result = conect.execute(text(sql))
    lst_med_adm = []
    for adm in result:
        if id in adm:
            lst_med_adm.append({'id': adm[0],
                                'Nome do Cliente': adm[1],
                                'Nome do Remedio': adm[2],
                                'Quantidade por Dia': adm[3],
                                'receipt_date': str(adm[4]),
                                'entry_quant': adm[5],
                                'perda': adm[6],
                                'expiration_date': str(adm[7]),
                                'paciente ativo': adm[8] })

    return JSONResponse(lst_med_adm)


def post_med_adm(db: Session, id_patient: str, id_med: str, quant_capsule_day: int,
                 receipt_date: date, entry_quant: int, loss: int, expiration_date: date):

    patient = get_patient(db, id_patient)
    if not patient or patient.is_active == False:
        raise HTTPException(status_code=401, detail="Paciente não existe no banco de dados")
    medicine = get_medicine(db, id_med)
    if not medicine:
        raise HTTPException(status_code=401, detail="Medicamento não existe no banco de dados")
    med_adm_create = Med_adm(id_patient=id_patient, id_med=id_med, quant_capsule_day=quant_capsule_day,
                                  receipt_date=receipt_date, entry_quant=entry_quant, loss=loss,
                                  expiration_date=expiration_date)
    db.add(med_adm_create)
    db.commit()
    db.refresh(med_adm_create)
    lista = {'id_patient':med_adm_create.id_patient,
             'id_medicamento': med_adm_create.id_med,
             'quantidade pro dia': med_adm_create.quant_capsule_day,
             'data de recebimento': str(med_adm_create.receipt_date),
             'quantidade recebida': med_adm_create.entry_quant,
             'perdas': med_adm_create.loss,
             'data de validade': str(med_adm_create.expiration_date)}
    return lista
