import mysql.connector
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2ZXdXJSnwlwVKk7553mP@containers-us-west-49.railway.app:6614/railway'
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
db = SQLAlchemy(app)
ma = marshmallow
mydb = mysql.connector.connect(
    host='containers-us-west-49.railway.app',
    user='root',
    password='2ZXdXJSnwlwVKk7553mP',
    port='6614')

cursor = mydb.cursor()