import mysql.connector
from flask import Flask
from flask_login import LoginManager
import marshmallow
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager(app)
ma = marshmallow

mydb = mysql.connector.connect(
    host='containers-us-west-50.railway.app',
    user='root',
    password='ZTaQxeQttlYLn77wJ6sb',
    port='6233',
    database='railway')

cursor = mydb.cursor()
