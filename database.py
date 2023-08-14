import mysql.connector
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:7hTknayAdiMlWMbuVzgI@containers-us-west-144.railway.app:6009/railway'
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
db = SQLAlchemy(app)
ma = marshmallow
mydb = mysql.connector.connect(
    host='containers-us-west-144.railway.app',
    user='root',
    password= '7hTknayAdiMlWMbuVzgI',
    database='railway')

cursor = mydb.cursor()