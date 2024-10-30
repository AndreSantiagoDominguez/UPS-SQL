# Importación de dependencias
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from models.user import User

db = SQLAlchemy()
load_dotenv()

# Definición de la clase donatarios
class Donee(User):
    schema_name = os.getenv("SCHEMA")
    pr


    def __init__(self, first_name, last_name, email, password, state, locality, distrit):
        super().__init__(first_name, last_name, email, password, state, locality, distrit)