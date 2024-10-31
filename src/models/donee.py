# Importación de dependencias
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from src.models.user import User, db
from sqlalchemy.dialects.postgresql import ARRAY

load_dotenv()

# Definición de la clase donatarios
class Donee(User):

    schema_name = os.getenv("SCHEMA")
    __tablename__ = 'donees'
    __table_args__ = {'schema': schema_name}

    id_donee = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('SCHEMA')}.users.id_user"), primary_key = True, autoincrement = True)
    id_list_donors = db.Column(ARRAY(db.Integer), nullable = False)
    #credentials = db.Column(ARRAY(db.String), nullable = False)

    def __init__(self, first_name, last_name, email, password, state, locality, distrit, list_contributions):
        #[ email, password ] = credentials
        print(email)
        super().__init__(first_name, last_name, email, password, state, locality, distrit)
        self.id_list_donors = list_contributions
        #self.credentials = credentials