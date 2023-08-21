import mysql.connector
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)
mydb = mysql.connector.connect(
    host='containers-us-west-50.railway.app',
    user='root',
    password='ZTaQxeQttlYLn77wJ6sb',
    port='6233',
    database='railway')

cursor = mydb.cursor()

