from sqlalchemy.types import TypeDecorator, VARCHAR

# Clase para el tipo compuesto access_credentials
class AccessCredentials(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Formato para tipo compuesto en PostgreSQL
            return f'("{value["email"]}", "{value["password"]}")'
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            # Convierte el valor de vuelta a diccionario
            email, password = value[1:-1].split(", ")
            return {"email": email.strip('"'), "password": password.strip('"')}
        return None

# Clase para el tipo compuesto address
class Address(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            return f'("{value["state"]}", "{value["locality"]}", "{value["distrit"]}")'
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            state, locality, distrit = value[1:-1].split(", ")
            return {"state": state.strip('"'), "locality": locality.strip('"'), "distrit": distrit.strip('"')}
        return None
