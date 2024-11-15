from datetime import timedelta
from flask import jsonify
from sqlalchemy import func
from src.models.donor import Donor, db, os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from googleapiclient.http import MediaFileUpload
from config import drive_service

def createDonor(data):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    try:
        # Obtener los datos
        newDonor = Donor(
            first_name,
            last_name,
            email,
            password,
            phone_number,    
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
        return jsonify({"mensaje": "No se entontró"}), 404

    if not donor.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    expires = timedelta(hours=2)
    access_token = create_access_token(identity=donor.id_donor, expires_delta=expires)
    
    return jsonify({"mensaje": "Inicio de sesión exitoso", "access_token": access_token}), 200

@jwt_required()  #Cuando quiere dar de baja su cuenta
def delete():
    try:
        donor_id_donor = get_jwt_identity()
        donor = Donor.query.get(donor_id_donor)
        if not Donor:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        
        db.session.delete(donor)
        db.session.commit()
        return jsonify({"msg": "Usuario eliminado"}), 200
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500
    
@jwt_required() 
def upload_to_drive(file_path, file_name):
    try:
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, resumable=True)
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        donor_id_donor = get_jwt_identity()  
        donor = Donor.query.get(donor_id_donor)

        id_photo = uploaded_file.get('id')
        donor.photo = id_photo
        db.session.commit()
        return id_photo
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def getLocalities():
    try:
        localitiesResponse = db.session.query(
            func.jsonb_extract_path_text(Donor.address, 'locality').label('locality')
        ).group_by(func.jsonb_extract_path_text(Donor.address, 'locality'))
        
        localities = [{'locality': locality} for (locality,) in localitiesResponse]
        return jsonify(localities)
    except Exception as e:
        return jsonify({ 'error': str(e)})
