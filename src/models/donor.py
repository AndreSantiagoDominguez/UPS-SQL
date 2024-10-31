# Importación de dependencias
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from models.user import User, db
from sqlalchemy.dialects.postgresql import ENUM
load_dotenv()

# Definición de la clase donatarios
class Donor(User):

    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'donors'
    __table_args__ = {'schema': schema_name}

    id_donor = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key = True, autoincrement = True)
    health_status = db.Column(ENUM('Good', 'Recovery', name="health_status_enum"), nullable=False)
    availability = db.Column(ENUM('morning', 'afternoon', name="availability_enum"), nullable=False)
    donations_number = db.Column(db.Integer, nullable = False)
    last_donation = db.Column(db.Date, nullable = False)

    def __init__(self, first_name, last_name, email, password, state, locality, distrit, health_status, availability, donations_number, last_donation):
        super().__init__(first_name, last_name, email, password, state, locality, distrit)
        self.health_status = health_status,
        self.availability = availability,
        self.donations_number = donations_number,
        last_donation = last_donation