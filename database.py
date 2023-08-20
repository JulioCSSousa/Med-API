import mysql.connector
from flask import Flask
from flask_login import LoginManager
import marshmallow
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager(app)
ma = marshmallow

mydb = mysql.connector.connect(
    host='containers-us-west-62.railway.app',
    user='root',
    password='aZH6GgpyuUfTnHJ9sc00',
    port='8871',
    database='railway')

cursor = mydb.cursor()
