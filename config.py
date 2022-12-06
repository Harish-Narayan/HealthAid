import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

current_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

DB_URL = 'postgresql+psycopg2://postgres:dbms@127.0.0.1:5432/package'
print(DB_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] ="filesystem"
Session(app)

print('success')
db = SQLAlchemy(app)
#db.init_app(app)
#db.app_context().push()

