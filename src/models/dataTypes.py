from sqlalchemy.types import TypeDecorator, String
import json

class AddressType(TypeDecorator):
    impl = String

    def __init__(self, state=None, locality=None, distrit=None, *args, **kwargs):
        # Aquí puedes almacenar estos valores o hacer algo con ellos
        self.state = state
        self.locality = locality
        self.distrit = distrit
        super().__init__(*args, **kwargs)
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps({
                'state': value.state,
                'locality': value.locality,
                'distrit': value.distrit
            })  # Convertir el objeto a JSON
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            data = json.loads(value)  # Convertir de JSON a objeto
            return AddressType(**data)  # Crear un nuevo objeto AddressType
        return None

class AccessCredentialsType(TypeDecorator):
    impl = String

    def __init__(self, email=None, password=None, *args, **kwargs):
        # Aquí puedes almacenar estos valores o hacer algo con ellos
        self.email = email
        self.password = password
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps({
                'email': value.email,
                'password': value.password
            })  # Convertir el objeto a JSON
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            data = json.loads(value)  # Convertir de JSON a objeto
            return AccessCredentialsType(**data)  # Crear un nuevo objeto AccessCredentialsType
        return None

