# Importación de dependencias
from geoalchemy2 import Geometry
from . import db
import os

class BloodBanks(db.Model):

    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'blood_banks'
    __table_args__ = {'schema': schema_name}

    id_blood_bank = db.Column(db.Integer, primary_key = True, autoincrement = True)
    location      = db.Column(Geometry(geometry_type='POINT', srid = 4326))

    details = db.relationship('DetailsBank', backref='blood_banks', lazy=True)