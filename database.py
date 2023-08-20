import mysql.connector
from flask import Flask
from flask_login import LoginManager
import marshmallow
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager(app)
ma = marshmallow

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='159753',
    port='3306',
    database='pymeddb')

cursor = mydb.cursor()
