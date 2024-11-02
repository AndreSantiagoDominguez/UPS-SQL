from sqlalchemy.types import TypeDecorator, VARCHAR

# Clase para el tipo compuesto access_credentials
class AccessCredentials(TypeDecorator):
    impl = VARCHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value:
            # Asegúrate de que el valor esté en el formato esperado para PostgreSQL
            return f'("{value["email"]}", "{value["password"]}")'
        return None

    def process_result_value(self, value, dialect):
        if value:
            print(f"Raw value from DB: {value}")
            try:
                # Eliminar paréntesis y espacios en los extremos
                clean_value = value.strip('() ')
                # Separar por comas, asegurando que la contraseña puede contener comas
                email, password = clean_value.split(", ", 1)  # Usa el segundo argumento para dividir una vez
                return {
                    "email": email.strip('"'),  # Eliminar comillas
                    "password": password.strip('"')
                }
            except ValueError as e:
                print(f"Error parsing value: {e}")
                return None
        return None



# Clase para el tipo compuesto address
class Address(TypeDecorator):
    impl = VARCHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return f'("{value["state"]}", "{value["locality"]}", "{value["distrit"]}")'
        return None

    def process_result_value(self, value, dialect):
        print("Processing result value:", value)  # Para ver el valor recibido
        if value:
            try:
                # Asegúrate de que el valor tiene el formato esperado
                parts = value[1:-1].split(", ")
                if len(parts) != 3:
                    raise ValueError(f"Expected 3 parts but got {len(parts)}: {parts}")
                state, locality, distrit = parts
                return {
                    "state": state.strip('"'),
                    "locality": locality.strip('"'),
                    "distrit": distrit.strip('"')
                }
            except ValueError as e:
                print("Error processing result value:", str(e))  # Detalle del error
                return None
        return None

