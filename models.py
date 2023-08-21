from database import login_manager, mydb, cursor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
from flask import jsonify


@login_manager.user_loader
def get_user(id):
    sql = f'SELECT * FROM users WHERE id = {id}'
    cursor.execute(sql)
    user = cursor.fetchall()
    return user


def generate_uuid():
    return str(uuid.uuid4())

class User(UserMixin):

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def get_hash(self, password):
        self.password = generate_password_hash(password)

    def register(self, name, email, password):
        sql = f'INSERT INTO users (id, name, email, password) VALUES ("{generate_uuid()}", "{name}' \
              f'"{email}", "{password}");'
        cursor.execute(sql)
        mydb.commit()
        return jsonify(message='Usuario cadastrado com sucesso')

    def verify_pwd(self, password):
        return check_password_hash(self.password, password)

