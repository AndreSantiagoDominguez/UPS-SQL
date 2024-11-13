# Importación de dependencias
from sqlalchemy import JSON, ForeignKey
from . import db
import os

class DetailsBank(db.Model):

    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'details_bank'
    __table_args__ = {'schema': schema_name}

    id_blood_bank = db.Column(db.Integer, ForeignKey(f'{schema_name}.blood_banks.id_blood_bank'), primary_key = True)
    name_place    = db.Column(db.String(50), nullable = False)
    phone_number  = db.Column(db.String(10), nullable = False)
    address       = db.Column(JSON, nullable = False)