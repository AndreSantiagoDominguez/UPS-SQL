from sqlalchemy.types import TypeDecorator, VARCHAR

class AccessCredentials(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Formato para el tipo compuesto en PostgreSQL
            return f'("{value.get("email", "")}", "{value.get("password", "")}")'
        return None

    def process_result_value(self, value, dialect):
        if value:
            try:
                email, password = value[1:-1].split(", ")
                return {"email": email.strip('"'), "password": password.strip('"')}
            except ValueError:
                # Retorna None o un valor por defecto si el formato no es válido
                return {"email": None, "password": None}
        return None

class Address(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            return f'("{value.get("state", "")}", "{value.get("locality", "")}", "{value.get("distrit", "")}")'
        return None

    def process_result_value(self, value, dialect):
        if value:
            try:
                state, locality, distrit = value[1:-1].split(", ")
                return {"state": state.strip('"'), "locality": locality.strip('"'), "distrit": distrit.strip('"')}
            except ValueError:
                # Retorna None o un valor por defecto si el formato no es válido
                return {"state": None, "locality": None, "distrit": None}
        return None
