import datetime
from flask import request, jsonify
from database import *
import jwt
from authenticate import jwt_required
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


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
    mydb.commit()
    mydb.commit()
    return jsonify()


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    cursor.execute(f'SELECT id, password FROM users WHERE email = "{email}";')
    list = cursor.fetchall()
    user = list[0][0]
    passwordbd = list[0][1]

    if not check_password_hash(passwordbd,password):
        return jsonify(message='Password inválido')

    payload = {
        "id": user,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return jsonify({"token": token})

"""@app.route('/logout')
def logout():
    logout_user()
    return ''"""


@app.route('/auth/protected', methods=['GET'])
@jwt_required
def protected(current_user):
    sql = 'SELECT name, email FROM users ;'
    cursor.execute(sql)
    list = cursor.fetchall()
    return jsonify(list)


#PATIENTS
@app.route('/patients', methods=['GET'])
@jwt_required
def get_patient(current_user):
    sql = ('SELECT * FROM patients;')
    cursor.execute(sql)
    lista = cursor.fetchall()
    return jsonify(lista)


@app.route('/patients', methods=['POST'])
@jwt_required
def insert_patient(current_user):
    name = request.json['patient_name']
    cpf = request.json['cpf']
    note = request.json['note']
    sql = f'INSERT INTO patients (id, patient_name, cpf, notes) VALUES ("UUID()", "{name}", "{cpf}", "{note}");'
    cursor.execute(sql)
    mydb.commit()
    return jsonify(message=f'{name} cadastrado com sucesso')

@app.route('/patients/<id>', methods=['GET'])
@jwt_required
def find_patient_id(current_user, id):
    sql = f'SELECT * FROM patients WHERE id = "{id}";'
    cursor.execute(sql)
    patient = cursor.fetchall()
    return jsonify(patient)

@app.route('/patients/<id>', methods=["PUT"])
@jwt_required
def edit_patient(current_user, id):
    name = request.json['patient_name']
    cpf = request.json['cpf']
    sql = f'UPDATE patients SET patient_name = "{name}", cpf = "{cpf}" WHERE id="{id}";'
    cursor.execute(sql)
    mydb.commit()
    return jsonify(message='Pacient editado com sucesso')


@app.route('/patients/<id>', methods=["DELETE"])
def delete_patient():
    pass



#MEDICAMENTOS

@app.route('/medicines', methods=['GET'])
@jwt_required
def get_med(current_user):
    sql = ('SELECT * FROM medicines;')
    cursor.execute(sql)
    lista = cursor.fetchall()
    return jsonify(lista)



@app.route('/medicines', methods=['POST'])
@jwt_required
def insert_med(current_user):
    name = request.json['med_name']
    quant = request.json['quant_capsule_box']
    sql = f'INSERT INTO medicines (id, med_name, quant_capsule_box) VALUES (UUID(), "{name}", "{quant}");'
    cursor.execute(sql)
    mydb.commit()
    return jsonify(message=f'{name} cadastrado com sucesso')


@app.route('/medicines/<id>', methods=['GET'])
@jwt_required
def get_med_id(id, current_user):
    sql = f'SELECT * FROM medicines WHERE id = {id};'
    cursor.execute(sql)
    patient = cursor.fetchall()
    return jsonify(patient)

@app.route('/medicines/<id>', methods=['PUT'])
@jwt_required
def med_edit(id, current_user):
    name = request.json['med_name']
    quant = request.json['quant_capsule_box']
    sql = f'UPDATE medicines SET med_name = "{name}", quant_capsule_da = {quant} WHERE id="{id}";'
    cursor.execute(sql)
    mydb.commit()
    return jsonify(message='Pacient editado com sucesso')

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
    cursor.execute("""SELECT patients.id, patients.patient_name, medicines.med_name, med_adm.quant_capsule_day, receipt_date, entry_quant, expiration_date
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
                            'receipt_date': adm[4],
                            'entry_quant': adm[5],
                            'expiration_date': adm[6] })
    return jsonify(lst_med_adm)


@app.route('/med-adm/<int:id>', methods=['GET'])
@jwt_required
def get_med_adm_id(id, current_user):
    cursor.execute("""SELECT patients.id, patients.patient_name, medicines.med_name, med_adm.quant_capsule_day, receipt_date, entry_quant, expiration_date
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
                            'receipt_date': adm[4],
                            'entry_quant': adm[5],
                            'expiration_date': adm[6] })
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




