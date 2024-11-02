from tokenize import String
from typing import cast
from flask import jsonify
from sqlalchemy import func, select, text
from src.models.donee import Donee, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def createDonee(data):
    try:
        print(data)
        # Obtener los datos
        newDonee = Donee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            state=data['state'],
            locality=data['locality'],
            distrit=data['distrit'],
            phone_number=data['phone_number']
        )

        print(newDonee)

        # Inserción 
        db.session.add(newDonee)
        db.session.commit()

        # resultado
        return jsonify({
            "msg": "Success",
            "id_donee": newDonee.id_donee
        }), 201
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500


def updateDonee(id_donee, data):
    try:
        # Buscar el donatario en la base de datos
        donee = Donee.query.get(id_donee)

        if not donee:
            return jsonify({"error": "Donee not found"}), 404

        if 'credentials' in data:
            credentials = data['credentials']

            if 'password' in credentials:
                credentials['password'] = Donee.hashNewPass(credentials['password'])

            setattr(donee, 'credentials', credentials)
                
        # Actualizar solo los atributos que se proporcionan en el data
        for key, value in data.items():
            if hasattr(donee, key) and key != 'credentials':
                setattr(donee, key, value)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "msg": "Donee updated successfully",
            "id_donee": donee.id_donee,
        }), 200
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

def login(data):
    email = data.get('email')
    password = data.get('password')

    donee = Donee.query.filter(func.jsonb_extract_path_text(Donee.credentials, 'email') == email).first()

    if not donee:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    if not donee.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    access_token = create_access_token(identity=donee.id_donee)
    
    return jsonify({"mensaje": "Inicio de sesión exitoso", "access_token": access_token}), 200


@jwt_required()
def obtener_usuario():
    Donee_id = get_jwt_identity()
    Donee = Donee.query.get(Donee_id)
    if not Donee:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
        return jsonify({
        "id": Donee.id,
         "nombre": Donee.nombre,
         "email": Donee.email
     }), 200

@jwt_required()
def eliminar_usuario(Donee_id):
    Donee = Donee.query.get(Donee_id)
    if not Donee:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    db.session.delete(Donee)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"}), 200
