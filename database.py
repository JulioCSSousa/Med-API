import mysql.connector
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4306@localhost/pymeddb'
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
db = SQLAlchemy(app)
ma = marshmallow
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password= '4306',
    database='pymeddb',)

cursor = mydb.cursor()