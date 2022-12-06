from config import app
from flask_sqlalchemy import SQLAlchemy
from config import db 
from controllers import *

if __name__=='__main__':
    app.run(debug=True,host='127.0.0.1',port='5000')