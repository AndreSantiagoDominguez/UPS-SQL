from flask import jsonify, send_from_directory
from sqlalchemy import func, text
from src.models.profile import Profile, db
from src.models.donor import Donor
from flask_jwt_extended import jwt_required, get_jwt_identity
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO
from config import drive_service
import json

def createProfile(data):
    try:
        # Obtener los datos
        bloodType = data.get('bloodType')
        id_donor = data.get('id_donor')

        if not bloodType:
            return jsonify({"error": "Falta campo requerido: el tipo de sangre"}), 400

        newProfile = Profile(id_donor=id_donor,bloodType=bloodType)

        # Inserción 
        db.session.add(newProfile)
        db.session.commit()

        # resultado
        return jsonify({
            "msg": "Success"
        }), 201
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

@jwt_required()
def updateProfile(data):
    try:
        # Buscar el donatario en la base de datos
        donor_id_donor = get_jwt_identity()
        profile = Profile.query.get(donor_id_donor)

        if not profile:
            return jsonify({"error": "Donor not found"}), 404
                
        # Actualizar solo los atributos que se proporcionan en el data
        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "msg": "Donor updated successfully",
        }), 200
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

@jwt_required()
def getProfile():
    donor_id_donor = get_jwt_identity()  

    donor_profile = db.session.query(Donor, Profile).filter(Donor.id_donor == Profile.id_donor).filter(Donor.id_donor == donor_id_donor).first()

    if not donor_profile:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    donor, profile = donor_profile  

    response = {
        'id_donor': donor.id_donor,
        'first_name': donor.first_name,
        'last_name': donor.last_name,
        'email': donor.credentials['email'],  
        'address': donor.address,
        'phone_number': donor.phone_number,
        'health_status': profile.health_status,
        'availability': profile.availability,
        'donations_number': profile.donations_number,
        'last_donation': profile.last_donation,
        'blood_type': profile.blood_type,
        'photo': donor.photo
    }

    return jsonify(response), 200

@jwt_required()
def get_photo():
    try: 
        donor_id_donor = get_jwt_identity()  
        donor = Donor.query.get(donor_id_donor)
        return download_from_drive(donor.photo)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def download_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    file_data = BytesIO()
    downloader = MediaIoBaseDownload(file_data, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_data.seek(0)
    return file_data
    
def get_photo_by_name(id_photo):
    try: 
        return download_from_drive(id_photo)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getProfileById(id_donor):
    donor_profile = db.session.query(Donor, Profile).filter(Donor.id_donor == Profile.id_donor).filter(Donor.id_donor == id_donor).first()

    if not donor_profile:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    donor, profile = donor_profile  

    response = {
        'id_donor': donor.id_donor,
        'first_name': donor.first_name,
        'last_name': donor.last_name,
        'email': donor.credentials['email'],  
        'address': donor.address,
        'phone_number': donor.phone_number,
        'health_status': profile.health_status,
        'availability': profile.availability,
        'donations_number': profile.donations_number,
        'last_donation': profile.last_donation,
        'blood_type': profile.blood_type,
        'photo': donor.photo
    }

    return jsonify(response), 200

# Para buscar
def searchByBloodType(bloodType):
    donors = db.session.query(Donor, Profile).filter(Donor.id_donor == Profile.id_donor).filter(Profile.blood_type == bloodType).limit(20).all()

    if not donors:
        return jsonify({"mensaje": "No se encontraron usuarios con ese tipo de sangre"}), 404

    response_list = []
    for donor, profile in donors:
        response = {
            'id_donor': donor.id_donor,
            'first_name': donor.first_name,
            'last_name': donor.last_name,
            'address': donor.address,
            'blood_type': profile.blood_type,
            'compatibility': compatibilityBlood(profile.blood_type)
        }
        response_list.append(response)

    return jsonify(response_list), 200

def searchByLocality(locality):
    donors = (
        db.session.query(Donor, Profile)
        .filter(Donor.id_donor == Profile.id_donor)
        .filter(func.jsonb_extract_path_text(Donor.address, 'locality') == locality)
        .limit(20)
        .all()
    )

    if not donors:
        return jsonify({"mensaje": "No se encontraron donadores en esta localidad"}), 404

    response_list = []
    for donor, profile in donors:
        response = {
            'id_donor': donor.id_donor,
            'first_name': donor.first_name,
            'last_name': donor.last_name,
            'address': donor.address,
            'blood_type': profile.blood_type,
            'compatibility': compatibilityBlood(profile.blood_type)
        }
        response_list.append(response)

    return jsonify(response_list), 200


with open('queries.json', 'r') as file:
    queries = json.load(file)

def searchByCompatibility(type):
    switch = {
        'A+': caseAp,
        'A-': caseAn,
        'B+': caseBp,
        'B-': caseBn,
        'AB+': caseABp,
        'AB-': caseABn,
        'O+': caseOp,
        'O-': caseOn,
    }
    
    return switch.get(type)()

def caseAp():
    query = text(queries['A+'])
    return response(query)

def caseAn():
    query = text(queries['A-'])
    return response(query)

def caseBp():
    query = text(queries['B+'])
    return response(query)

def caseBn():
    query = text(queries['B-'])
    return response(query)

def caseABp():
    query = text(queries['AB+'])
    return response(query)

def caseABn():
    query = text(queries['AB-'])
    return response(query)

def caseOp():
    query = text(queries['O+'])
    return response(query)

def caseOn():
    query = text(queries['O-'])
    return response(query)

def response(query):
    result = db.session.execute(query)
    
    # Recuperar los resultados
    donors = result.fetchall()

    if not donors:
        return jsonify({"mensaje": "No se encontraron donadores compatibles"}), 404
    donors_list = []
    for donor in donors:
        compatibility = compatibilityBlood(donor[4])
        donors_list.append({
            'id_donor': donor[0],
            'first_name': donor[1],
            'last_name': donor[2],
            'address': donor[3],
            'blood_type': donor[4],
            'compatibility': compatibility
        })
    return jsonify(donors_list), 200

def compatibilityBlood(type):
    if(type == 'A+'):
        return ['A+','A-','O+','O-']
    if(type == 'A-'):
        return ['A-','O-']
    if(type == 'B+'):
        return ['B+','B-','O+','O-']
    if(type == 'B-'):
        return ['B-','O-']
    if(type == 'AB+'):
        return ['All'] 
    if(type == 'AB-'):
        return ['A-','B-','AB-','O-']
    if(type == 'O+'):
        return ['O+','O-']
    if(type == 'O-'):
        return ['O-']   