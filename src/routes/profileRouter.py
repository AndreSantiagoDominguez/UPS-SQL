from flask import Blueprint, request, send_file
from src.controllers.profileController import createProfile, updateProfile, getProfile, getProfileById, searchByBloodType, searchByLocality, get_photo

profileBlueprint = Blueprint('profile', __name__)

@profileBlueprint.route('/add', methods=['POST'])
def addProfile():
    data = request.get_json()
    return createProfile(data)

@profileBlueprint.route('/update', methods=['PUT'])
def putProfile():
    data = request.get_json()
    return updateProfile(data)

@profileBlueprint.route('/profile', methods=['GET'])
def viewProfile():
    return getProfile()

@profileBlueprint.route('/photo', methods=['GET'])
def download_drive():
    file_data = get_photo()
    return send_file(file_data, mimetype='image/jpeg')

@profileBlueprint.route('/photo/<string:id_photo>', methods=['GET'])
def viewPhotoName(name):
    file_data = get_photo(name)
    return send_file(file_data, mimetype='image/jpeg')

@profileBlueprint.route('/search/<int:id_donor>', methods=['GET'])
def search(id_donor):
    return getProfileById(id_donor)

@profileBlueprint.route('/searchByLocality/<string:locality>', methods=['GET'])
def ByLocality(locality):
    return searchByLocality(locality)

@profileBlueprint.route('/searchByBlood/<string:type>', methods=['GET'])
def searchByBlood(type):
    return searchByBloodType(type)
