from datetime import timedelta
from flask import jsonify
from sqlalchemy import func
from src.models.donee import Donee, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def createDonee(data):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    
    try:
        # Obtener los datos
        newDonee = Donee(
            first_name,
            last_name,
            email,
            password,
            phone_number,
        )

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

@jwt_required()
def updateDonee(data):
    try:
        donee_id_donee = get_jwt_identity()
        donee = Donee.query.get(donee_id_donee)
        print(donee)
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
        print(donee)
        return jsonify({
            "msg": "Donee updated successfully",
            "id_donee": donee.id_donee
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
        return jsonify({"mensaje": "No se entontró"}), 404

    if not donee.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    expires = timedelta(hours=2)
    access_token = create_access_token(identity=donee.id_donee, expires_delta=expires)
    
    return jsonify({"mensaje": "Inicio de sesión exitoso", "access_token": access_token}), 200

@jwt_required()
def getDonee():
    donee_id_donee = get_jwt_identity()
    donee = Donee.query.get(donee_id_donee)
    if not Donee:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    return jsonify({
        'id_donee': donee.id_donee,
        'first_name': donee.first_name,
        'last_name': donee.last_name,
        'email': donee.credentials['email'],
        'address': donee.address,
        'phone_number': donee.phone_number
    }), 200


def getDoneeById(id_donee):
    donee = Donee.query.get(id_donee)
    if not Donee:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    return jsonify({
        'id_donee': donee.id_donee,
        'first_name': donee.first_name,
        'last_name': donee.last_name,
        'email': donee.credentials['email'],
        'address': donee.address,
        'phone_number': donee.phone_number
    }), 200

@jwt_required()  #Cuando quiere dar de baja su cuenta
def delete():
    donee_id_donee = get_jwt_identity()
    donee = Donee.query.get(donee_id_donee)
    if not Donee:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    db.session.delete(donee)
    db.session.commit()
    return jsonify({"msg": "Usuario eliminado"}), 200
