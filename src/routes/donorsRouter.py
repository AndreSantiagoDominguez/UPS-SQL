import os
import tempfile
from flask import Blueprint, jsonify, request
from src.controllers.donorsController import createDonor, updateDonor, login, delete, upload_to_drive, getLocalities

donorsBlueprint = Blueprint('donors', __name__)

@donorsBlueprint.route('/add', methods=['POST'])
def addDonor():
    data = request.get_json()
    return createDonor(data)

@donorsBlueprint.route('/update', methods=['PUT'])
def putDonor():
    data = request.get_json()
    return updateDonor(data)

@donorsBlueprint.route('/login', methods=['POST'])
def loginR():
    data = request.get_json()
    return login(data)

@donorsBlueprint.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return delete()

@donorsBlueprint.route('/addPhoto', methods=['POST'])
def upload_drive():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['photo']
    file_name = file.filename
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file_name)      #f'/tmp/{file_name}'
    file.save(file_path)

    file_id = upload_to_drive(file_path, file_name)
    google_drive_url = file_id  # f"https://drive.google.com/uc?id={file_id}"

    # Guardar el file_id en un archivo JSON
    # data = {}
    # if os.path.exists('file_ids.json'):
    #     with open('file_ids.json', 'r') as f:
    #         data = json.load(f)

    # data[file_name] = file_id
    # with open('file_ids.json', 'w') as f:
    #     json.dump(data, f)

    os.remove(file_path)

    return jsonify({'google_drive_url': google_drive_url}), 200

@donorsBlueprint.route('/localities', methods=['GET'])
def getAllLocalities():
    return getLocalities()