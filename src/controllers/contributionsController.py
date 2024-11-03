from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from src.models.contributions import db, Contributions
from src.models.donor import Donor
from src.models.profile import Profile

def createContribution(data):
    try:
        id_donee = data.get('id_donee')
        id_donor = data.get('id_donor')

        if not id_donee or not id_donor:
            return jsonify({"mensaje": "Faltan atributos"}), 400

        newContribution = Contributions(id_donor=id_donor, id_donee=id_donee)

        # Agrega y guarda la nueva contribución en la base de datos
        db.session.add(newContribution)
        db.session.commit()
        return jsonify({"mensaje": "Contribución añadida exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Error al añadir la contribución", "error": str(e)}), 500
    
def getDonor():
    try:
        donee_id_donee = get_jwt_identity()

        result = db.session.query(
            Donor.first_name,
            Profile.blood_type
        ).join(
            Contributions, Donor.id_donor == Contributions.donor_id
        ).join(
            Profile, Donor.id_donor == Profile.id_donor
        ).filter(
            Contributions.id_donee == donee_id_donee
        ).all()

        response = [
            {
                'first_name': donor.first_name,
                'blood_type': donor.blood_type
            }
            for donor in result
        ]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la información", "error": str(e)}), 500
