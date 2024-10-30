# Importamos las dependencias
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import json
from sqlalchemy import JSON
db = SQLAlchemy()
bcrypt = Bcrypt()
load_dotenv()  

class User(db.Model):    

    schema_name = os.getenv('SCHEMA')
    print(schema_name)
    __tablename__ = 'users'
    __table_args__ = {'schema': schema_name}

    id_user = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    credentials = db.Column(JSON, nullable = False)
    address = db.Column(JSON, nullable = False)

    def __init__(self, first_name, last_name, email, password, state, locality, distrit):
        self.first_name = first_name
        self.last_name = last_name
        self.address = {'state': state, 'locality': locality, 'distrit': distrit}
        self.credentials = {'email': email, 'password': bcrypt.generate_password_hash(password).decode('utf-8')}

    def check_password(self, password):
        return bcrypt.check_password_hash(self.credentials['password'], password)

    def __repr__(self):
        return f'<User {self.first_name}>'

