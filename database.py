import mysql.connector
from flask import Flask
from flask_login import LoginManager
import marshmallow
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager(app)
ma = marshmallow

mydb = mysql.connector.connect(
    host='containers-us-west-49.railway.app',
    user='root',
    password='2ZXdXJSnwlwVKk7553mP',
    port='6614')

cursor = mydb.cursor()
