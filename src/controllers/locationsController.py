from flask import jsonify
from sqlalchemy import func
from src.models.bloodBanks import BloodBanks, db
from src.models.detailsBank import DetailsBank
from geoalchemy2.functions import ST_X, ST_Y

def getLocations(): 
    try:
        locations = (
            db.session.query(
                ST_X(func.ST_AsText(BloodBanks.location)).label('longitude'),
                ST_Y(func.ST_AsText(BloodBanks.location)).label('latitude'),
                DetailsBank.name_place,
                BloodBanks.id_blood_bank
            )
            .join(BloodBanks, BloodBanks.id_blood_bank == DetailsBank.id_blood_bank)
            .all()
        )

        locations_list = [
            {
            "longitude": result[0],
            "latitude": result[1],
            "name_place": result[2],
            "id_blood_bank": result[3]
            }
            for result in locations
        ]

        return jsonify(locations_list), 201
    
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500
    
def getDetailsLocation(id_blood_bank):
    try:
        details = DetailsBank.query.get(id_blood_bank)
        
        if not details:
            return jsonify({"mensaje": "No se entontró"}), 404

        detailsLocation = {
            'name_place': details.name_place,
            'address': details.address,
            'phone_number': details.phone_number
        }

        return jsonify(detailsLocation), 200
    
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500