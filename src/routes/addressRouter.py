from flask import jsonify, Blueprint
import requests, os

addressBlueprint = Blueprint('address', __name__)

@addressBlueprint.route('/<string:cp>', methods=['GET'])
def get_data(cp):
    api_key = os.getenv('APIKEY')
    try:
        headers = {
            'APIKEY': api_key
        }

        response = requests.get(
            'https://api.tau.com.mx/dipomex/v1/codigo_postal?cp='+cp,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()

            return jsonify({
                'postal_code': data.get('codigo_postal').get('codigo_postal'),
                'state': data.get('codigo_postal').get('estado'),
                'locality': data.get('codigo_postal').get('municipio'),
                'distrits': data.get('codigo_postal').get('colonias')
            })    
        else:
            return jsonify({'error': 'Error al obtener datos de la API externa'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

