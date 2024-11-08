from flask import jsonify, send_from_directory
from src.models.profile import Profile, db
from src.models.donor import Donor
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def createProfile(data):
    try:
        #Obtener id de la sesion
        donor_id_donor = get_jwt_identity()

        # Obtener los datos
        bloodType = data.get('bloodType')

        if not bloodType:
            return jsonify({"error": "Falta campo requerido: el tipo de sangre"}), 400

        newProfile = Profile(id_donor=donor_id_donor,bloodType=bloodType)

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
        'blood_type': profile.blood_type
    }

    return jsonify(response), 200

@jwt_required()
def get_photo():
    from app import create_app  
    app = create_app()

    try: 
        donor_id_donor = get_jwt_identity()
        donor = Donor.query.get(donor_id_donor)
        return send_from_directory(app.config['UPLOAD_FOLDER'], donor.photo)
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
        'blood_type': profile.blood_type
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
            'blood_type': profile.blood_type
        }
        response_list.append(response)

    return jsonify(response_list), 200

def searchByLocality(locality):
    donors = db.session.query(Donor, Profile).filter(Donor.id_donor == Profile.id_donor).filter(Donor.address['locality'] == locality).limit(20).all()

    if not donors:
        return jsonify({"mensaje": "No se encontraron usuarios con ese tipo de sangre"}), 404

    response_list = []
    for donor, profile in donors:
        response = {
            'id_donor': donor.id_donor,
            'first_name': donor.first_name,
            'last_name': donor.last_name,
            'address': donor.address,
            'blood_type': profile.blood_type
        }
        response_list.append(response)

    return jsonify(response_list), 200