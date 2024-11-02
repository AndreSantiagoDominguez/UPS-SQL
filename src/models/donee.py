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

# Definición de la clase donatarios
class Donee(db.Model):
    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'donees'
    __table_args__ = {'schema': schema_name}

    id_donee = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    credentials = db.Column(JSON, nullable=False) 
    address = db.Column(JSON, nullable=False)     
    phone_number = db.Column(db.String(10), nullable=False)

    def __init__(self, first_name, last_name, email, password, state, locality, distrit, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = {'state': state, 'locality': locality, 'distrit': distrit}
        self.credentials = {'email': email, 'password': bcrypt.generate_password_hash(password).decode('utf-8')}
        
    def check_password(self, password):
        passwordOF = self.credentials.get('password')
        return bcrypt.check_password_hash(passwordOF, password)
    
    def hashNewPass(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        email = self.credentials.get('email')
        return f'<User {self.first_name}, {email}>'
