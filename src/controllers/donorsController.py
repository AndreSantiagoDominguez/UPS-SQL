from datetime import timedelta
from flask import jsonify
from sqlalchemy import func
from src.models.donor import Donor, db, os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

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
    donor_id_donor = get_jwt_identity()
    donor = Donor.query.get(donor_id_donor)
    if not Donor:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    db.session.delete(donor)
    db.session.commit()
    return jsonify({"msg": "Usuario eliminado"}), 200

@jwt_required() 
def add_photo(photo):
    from app import create_app  
    app = create_app()
    try:    
        if not photo:
            return jsonify({"error": "No file uploaded"}), 400
        
        MAX_FILE_SIZE = 4 * 1024 * 1024  # 4 MB

        file_size = len(photo.read())  # Esto nos da el tamaño del archivo en bytes
        photo.seek(0) 

        # Verificar si el archivo excede el límite
        if file_size > MAX_FILE_SIZE:
           return jsonify({"msg": "El archivo es demasiado grande. El tamaño máximo permitido es de 10 MB."}), 400
        
        donor_id_donor = get_jwt_identity()  
        donor = Donor.query.get(donor_id_donor)

        filename = secure_filename(str(donor.id_donor)+photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        photo.save(filepath)

        if not donor:
            return jsonify({"error": "Donor not found"}), 404

        donor.photo = filename
        db.session.commit()

        return jsonify({"msg": "Photo uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
