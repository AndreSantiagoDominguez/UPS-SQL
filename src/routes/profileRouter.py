from flask import Blueprint, request
from src.controllers.profileController import createProfile, updateProfile, getProfile, getProfileById, searchByBloodType, searchByLocality, get_photo, getPhotoByName

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
def viewPhoto():
    return get_photo()

@profileBlueprint.route('/photo/<string:name>', methods=['GET'])
def viewPhotoName(name):
    return getPhotoByName(name)

@profileBlueprint.route('/search/<int:id_donor>', methods=['GET'])
def search(id_donor):
    return getProfileById(id_donor)

@profileBlueprint.route('/searchByLocality/<string:locality>', methods=['GET'])
def searchByLocality(locality):
    return searchByLocality(locality)

@profileBlueprint.route('/searchByBlood/<string:type>', methods=['GET'])
def searchByBlood(bloodtype):
    return searchByBloodType(bloodtype)
