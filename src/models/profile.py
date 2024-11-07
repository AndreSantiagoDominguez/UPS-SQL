# Importación de dependencias
from src.models.initDB import db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import ENUM
import os
bcrypt = Bcrypt()
load_dotenv()  

# Definición de la clase donatarios
class Profile(db.Model):

    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'profile'
    __table_args__ = {'schema': schema_name}

    id_donor = db.Column(db.Integer, db.ForeignKey('donors.id_donor'), primary_key=True)
    health_status = db.Column(ENUM('good', 'recovery', name="health_status_enum"), nullable=False, default='good')
    availability = db.Column(ENUM('morning', 'afternoon', name="availability_enum"), nullable=False, default='morning')
    blood_type = db.Column(ENUM(
        'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-',
        name="blood_type_enum"), nullable=False, unique=True, default='O-')
    donations_number = db.Column(db.Integer, nullable = False, default=0)
    last_donation = db.Column(db.Date, nullable = False, default='0000-00-00')

    def __init__(self, health_status, availability, donations_number, last_donation):
        self.health_status = health_status
        self.availability = availability
        self.donations_number = donations_number
        self.last_donation = last_donation