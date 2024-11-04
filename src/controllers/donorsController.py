from datetime import timedelta
from flask import jsonify
from sqlalchemy import func
from src.models.donor import Donor, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def createDonor(data):
    try:
        # Obtener los datos
        newDonor = Donor(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            state=data['state'],
            locality=data['locality'],
            distrit=data['distrit'],
            phone_number=data['phone_number']
        )

        # Inserción 
        db.session.add(newDonor)
        db.session.commit()

        # resultado
        return jsonify({
            "msg": "Success",
            "id_donor": newDonor.id_donor
        }), 201
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

@jwt_required()
def updateDonor(data):
    try:
        # Buscar el donatario en la base de datos
        donor_id_donor = get_jwt_identity()
        donor = Donor.query.get(donor_id_donor)

        if not donor:
            return jsonify({"error": "Donor not found"}), 404

        if 'credentials' in data:
            credentials = data['credentials']

            if 'password' in credentials:
                credentials['password'] = Donor.hashNewPass(credentials['password'])

            setattr(donor, 'credentials', credentials)
                
        # Actualizar solo los atributos que se proporcionan en el data
        for key, value in data.items():
            if hasattr(donor, key) and key != 'credentials':
                setattr(donor, key, value)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "msg": "Donor updated successfully",
            "id_donor": donor.id_donor,
        }), 200
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

def login(data):
    email = data.get('email')
    password = data.get('password')

    donor = Donor.query.filter(func.jsonb_extract_path_text(Donor.credentials, 'email') == email).first()

    if not donor:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    if not donor.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    expires = timedelta(hours=2)
    access_token = create_access_token(identity=donor.id_donor, expires_delta=expires)
    
    return jsonify({"mensaje": "Inicio de sesión exitoso", "access_token": access_token}), 200

@jwt_required()  #Cuando quiere dar de baja su cuenta
def delete():
    donor_id_donor = get_jwt_identity()
    donor = Donor.query.get(donor_id_donor)
    if not Donor:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    db.session.delete(donor)
    db.session.commit()
    return jsonify({"msg": "Usuario eliminado"}), 200
