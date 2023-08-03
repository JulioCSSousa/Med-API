from database import db, login_manager, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
@login_manager.user_loader

def get_user(user_id):
    return User.query.filter_by(id=user_id).first()
def generate_uuid():
    return str(uuid.uuid4())

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_name', 'cpf')

class MedicineSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'quant')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)
patient_share_schema = PatientSchema()
patients_share_schema = PatientSchema(many=True)
medicine_share_schema = MedicineSchema()
medicines_share_schema = MedicineSchema(many=True)


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.String(36), name='id', primary_key=True,  default=generate_uuid)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_pwd(self, password):
        return check_password_hash(self.password, password)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    patient_name = db.Column(db.String(64), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    notes = db.Column(db.Text)

    def __init__(self, name, cpf, notes):
        self.patient_name = name
        self.cpf = cpf
        self.notes = notes

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    med_name = db.Column(db.String(64), nullable=False)
    quant_capsule_box = db.Column(db.String(11), nullable=False, unique=True)

    def __init__(self, med_name, quant_capsule_box):
        self.med_name = med_name
        self.quant = quant_capsule_box