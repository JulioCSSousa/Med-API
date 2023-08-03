import datetime
from flask_login import logout_user
from flask import jsonify, request

from database import *
from models import users_share_schema, user_share_schema, patients_share_schema, patient_share_schema,\
    medicines_share_schema, medicine_share_schema
from models import User, Patient, Medicine
import jwt
from authenticate import jwt_required
import os
app.config['JSON_SORT_KEYS'] = False
path = os.environ["PATH"]
print(path)
database_url = os.environ.get("DATABASE_URL", "localhost")
print(database_url)
#trazer todos os remédios que estão vencendo
# data atual - data de recebimento * qt diaria - qt de percas
#Login Rotas


@app.route('/home')
def home():
    return 'Pagina Inicial'

@app.route('/register', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    user = User(name, email, password)
    user.verify_pwd(password)
    db.session.add(user)
    db.session.commit()
    result = user_share_schema.dump(
        User.query.filter_by(email=email).first()
    )
    return jsonify(result)


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first_or_404()

    if not user.verify_pwd(password):
        return jsonify({"error": "autenticação"}), 403

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return jsonify({"token": token})

@app.route('/logout')
def logout():
    logout_user()
    return ''


@app.route('/auth/protected', methods=['GET'])
@jwt_required
def protected(current_user):
    result = users_share_schema.dump(
        User.query.all()
    )

    return jsonify(result)


#PATIENTS
@app.route('/patients', methods=['GET'])
@jwt_required
def get_patient(current_user):
    patients = patients_share_schema.dump(
        Patient.query.all()
    )
    return jsonify(patients)


@app.route('/patients', methods=['POST'])
@jwt_required
def insert_patient(current_user):
    name = request.json['name']
    cpf = request.json['cpf']
    note = request.json['note']
    patient = Patient(name, cpf, note)
    db.session.add(patient)
    db.session.commit()
    return jsonify(message='Paciente cadastrado com sucesso! ')

@app.route('/patients/<id>', methods=['GET'])
@jwt_required
def find_patient_id(current_user, id):
    patient = patient_share_schema.dump(
        Patient.query.filter_by(id=id).first())
    if not patient:
        return jsonify(message='paciente não encontrado')


    return jsonify(patient)


@app.route('/patients/<id>', methods=["PUT"])
@jwt_required
def patient_edit_id(id,current_user):
    name = request.json['name']
    cpf = request.json['cpf']
    note = request.json['note']
    patient = Patient.query.filter_by(id=id).first()
    patient.client_name = name
    db.session.commit()
    patient.cpf = cpf
    db.session.commit()
    patient.notes = note
    db.session.commit()

    return jsonify(message="Paciente alterado com sucesso")


@app.route('/patients/<id>', methods=["DELETE"])
@jwt_required
def patient_del_id(current_user, id):
    Patient.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify(message='Paciente deletado')




#MEDICAMENTOS

@app.route('/medicines', methods=['GET'])
@jwt_required
def get_med(current_user):
    med = medicines_share_schema.dump(
        Medicine.query.all()
    )
    return jsonify(med)



@app.route('/medicines', methods=['POST'])
@jwt_required
def insert_med(current_user):
    medicine = request.json
    sql = f"INSERT INTO medicines (id, med_name, quant_capsule_box ) VALUES (UUID(), '{medicine['med_name']}', '{medicine['quant_capsule_box']}')"
    cursor.execute(sql)
    mydb.commit()
    return jsonify(
        message='medicamento cadastrado com sucesso',
        med=medicine
    )


@app.route('/medicines/<id>', methods=['GET'])
@jwt_required
def get_med_id(id, current_user):
    cursor.execute(f'select * from medicines where id = ("{id}")')
    med_list = cursor.fetchall()
    sort = []
    for item in med_list:
        sort.append({'Nome': item[1], 'Quantidade_Caixa': item[2]})
    return jsonify(med_list)

@app.route('/medicines/<id>', methods=['PUT'])
@jwt_required
def med_edit(id, current_user):
    med = request.json
    cursor.execute(f"SELECT * from medicines where id = ('{id}')")
    before = cursor.fetchall().copy()
    cursor.execute(f"UPDATE medicines SET med_name = '{med ['med_name']}', quant_capsule_box = '{med['quant_capsule_box']}' WHERE (`id` = '{id}');")
    mydb.commit()
    message = f"Mudanças: {before[0][1], before[0][2]} --> {med['med_name'], med['quant_capsule_box']}"
    return jsonify(message)

@app.route('/medicines/<int:id>', methods=["DELETE"])
@jwt_required
def med_del_id(id):
    sql = f"DELETE FROM medicines where id = {id};"
    cursor.execute(sql)
    mydb.commit()
    return jsonify(message='Medicamento deletado com sucesso')

#MED ADM

@app.route('/med-adm', methods=['GET'])
@jwt_required
def get_med_adm(current_user):
    cursor.execute("""SELECT patients.id, patients.client_name, medicines.med_name, med_adm.quant_capsule_day, med_adm.start_date
                      FROM patients
                      JOIN med_adm
                      ON patients.id = med_adm.id_patient
                      JOIN medicines
                      ON medicines.id = med_adm.id_med;""")
    med_adm_list = cursor.fetchall()
    lst_med_adm = []
    for adm in med_adm_list:
        lst_med_adm.append({'Nome do Cliente': adm[1],
                            'Nome do Remedio': adm[2],
                            'Quantidade por Dia': adm[3],
                            'inicio Medicação': adm[4]})
    return jsonify(lst_med_adm)


@app.route('/med-adm/<int:id>', methods=['GET'])
@jwt_required
def get_med_adm_id(id, current_user):
    cursor.execute("""SELECT patients.id, patients.client_name, medicines.med_name, med_adm.quant_capsule_day, med_adm.start_date
                      FROM patients
                      JOIN med_adm
                      ON patients.id = med_adm.id_patient
                      JOIN medicines
                      ON medicines.id = med_adm.id_med;""")
    med_adm_list = cursor.fetchall()
    lst_med_adm = []
    for adm in med_adm_list:
        lst_med_adm.append({'Id': adm[0],
                            'Nome do Cliente': adm[1],
                            'Nome do Remedio': adm[2],
                            'Quantidade por Dia': adm[3],
                            'Data de inicio': adm[4]})
    return jsonify(lst_med_adm[id-1])


@app.route('/med-adm', methods=(['POST']))
@jwt_required
def insert_med_adm(current_user):
    try:
        med_data = request.json
        sql = f"INSERT INTO patients (id, client_name, cpf) VALUES (UUID(), '{med_data['client_name']}', '{med_data['cpf']}');"
        cursor.execute(sql)
        mydb.commit()
        sql = f"select id from patients where cpf = '{med_data['cpf']}';"
        cursor.execute(sql)
        patient_id = cursor.fetchall()
        for med, quant, date_time, entry_quant, loss, expiration_date in zip(med_data['id_med'], med_data['quant_capsule_day'], med_data['start_date'],
                                                                             med_data['entry_quant'], med_data['loss'], med_data['expiration_date']):
            cursor.execute(f"INSERT INTO med_adm (id, id_patient, id_med, quant_capsule_day, "
                           f"start_date, entry_quant, loss, expiration_date) VALUES (UUID(),'{patient_id[0][0]}', "
                           f"'{med}', {quant}, '{date_time}', {entry_quant}, {loss}, '{expiration_date}')")

            mydb.commit()
    except mysql.connector.errors.IntegrityError:
        return jsonify(message='CPF Já existe')
    else:
        return jsonify(message='Cadastrado com sucesso')

@app.route('/med-adm/<id_patient>', methods=['POST'])
@jwt_required
def bondpxr(id_patient, current_user):
    #1 - Selecionar paciente
    #2 - vincular paciente com lista de remedio
    med_data = request.json
    sql = f"select * from patients where id = '{id_patient}';"
    cursor.execute(sql)
    patient_id = cursor.fetchall()
    for med, quant, date_time, entry_quant, loss, expiration_date in zip(med_data['id_med'], med_data['quant_capsule_day'], med_data['start_date'],
                                                                         med_data['entry_quant'], med_data['loss'], med_data['expiration_date']):
        cursor.execute(
            f"INSERT INTO med_adm (id, id_patient, id_med, quant_capsule_day, start_date, "
            f"entry_quant, loss, expiration_date ) VALUES (UUID(), '{patient_id[0][0]}', "
            f"'{med}', {quant}, '{date_time}', {entry_quant}, {loss}, '{expiration_date}')")
        mydb.commit()

    return(jsonify(message='Paciente e remedios vinculado com sucesso'))

@app.route('/med-adm/<id>', methods=(['DELETE']))
@jwt_required
def delete_med_adm_id(id, current_user):
    cursor.execute(f"DELETE FROM med_adm WHERE ('id' == {id})")
    mydb.commit()
    return jsonify(message='Paciente deletado com sucesso')

@app.route('/dates', methods=['GET'])
@jwt_required
def expiration(current_user):
    sql = """SELECT id_patient, patients.client_name, id_med, medicines.med_name, expiration_date from med_adm 
    JOIN patients on patients.id = med_adm.id_patient
    JOIN medicines ON medicines.id = med_adm.id_med
    AND expiration_date <= DATE_ADD(NOW(), INTERVAL 1 MONTH) AND expiration_date >= NOW();"""
    cursor.execute(sql)
    expiration = cursor.fetchall()
    sort = []
    for idp, np, idm, nm, validade in expiration:
        sort.append({
            "id do paciente": idp,
            "id do medicamento": idm,
            "nome do paciente": np,
            "nome do medicamento": nm,
            "validade": validade

        })
    return(sort)




app.run()
app.cursor.close()
app.mydb.close()




