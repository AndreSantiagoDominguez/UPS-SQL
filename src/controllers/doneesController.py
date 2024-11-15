from datetime import timedelta
from flask import jsonify, send_from_directory
from sqlalchemy import func
from src.models.donee import Donee, db, os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO
from config import drive_service

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
    try: 
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
            'phone_number': donee.phone_number,
            'photo': donee.photo
        }), 200
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

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
        'phone_number': donee.phone_number,
        'photo': donee.photo
    }), 200

@jwt_required()  #Cuando quiere dar de baja su cuenta
def delete():
    try:
        donee_id_donee = get_jwt_identity()
        donee = Donee.query.get(donee_id_donee)
        if not Donee:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        
        db.session.delete(donee)
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

        donee_id_donee = get_jwt_identity()  
        donee = Donee.query.get(donee_id_donee)

        id_photo = uploaded_file.get('id')
        donee.photo = id_photo
        db.session.commit()
        return id_photo
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@jwt_required()
def get_photo():
    try: 
        donee_id_donee = get_jwt_identity()  
        donee = Donee.query.get(donee_id_donee)
        return download_from_drive(donee.photo)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def download_from_drive(file_id):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        file_data = BytesIO()
        downloader = MediaIoBaseDownload(file_data, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        file_data.seek(0)
        return file_data
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500
    
def get_photo_by_name(id_photo):
    try: 
        return download_from_drive(id_photo)
    except Exception as e:
        return jsonify({"error": str(e)}), 500