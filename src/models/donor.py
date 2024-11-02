# Importamos las dependencias
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from src.models.dataTypes import AccessCredentials, Address
import os
db = SQLAlchemy()
bcrypt = Bcrypt()
load_dotenv()  

# Definición de la clase donatarios
class Donor(db.Model):

    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'donors'
    __table_args__ = {'schema': schema_name}

    id_donor = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    credentials = db.Column(AccessCredentials, nullable = False)
    address = db.Column(Address, nullable = False)
    phone_number = db.Column(db.String(10), nullable = False)

    def __init__(self, first_name, last_name, email, password, state, locality, distrit, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.address = {'state': state, 'locality': locality, 'distrit': distrit}
        self.credentials = {'email': email, 'password': bcrypt.generate_password_hash(password).decode('utf-8')}
        self.phone_number = phone_number

    def check_password(self, password):
        return bcrypt.check_password_hash(self.credentials['password'], password)

    def __repr__(self):
        return f'<User {self.first_name}>'