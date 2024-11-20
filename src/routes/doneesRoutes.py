import os
import tempfile
from flask import Blueprint, json, jsonify, request, send_file
from src.controllers.doneesController import createDonee, updateDonee, login, getDonee, delete, getDoneeById, get_photo, get_photo_by_name, upload_to_drive

doneesBlueprint = Blueprint('donees', __name__)

@doneesBlueprint.route('/add', methods=['POST'])
def addDonee():
    data = request.get_json()
    return createDonee(data)

@doneesBlueprint.route('/update', methods=['PUT'])
def putDonee():
    data = request.get_json()
    return updateDonee(data)

@doneesBlueprint.route('/login', methods=['POST'])
def loginR():
    data = request.get_json()
    return login(data)

@doneesBlueprint.route('/profile', methods=['GET'])
def viewProfile():
    return getDonee()

@doneesBlueprint.route('/search/<int:id_donee>', methods=['GET'])
def search(id_donee):
    return getDoneeById(id_donee)

@doneesBlueprint.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return delete()

@doneesBlueprint.route('/addPhoto', methods=['POST'])
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

@doneesBlueprint.route('/photo', methods=['GET'])
def download_drive():
    file_data = get_photo()
    return send_file(file_data, mimetype='image/jpeg')

@doneesBlueprint.route('/photo/<string:id_photo>', methods=['GET'])
def viewPhotoName(id_photo):
    file_data = get_photo(id_photo)
    return send_file(file_data, mimetype='image/jpeg')