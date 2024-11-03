from flask import Blueprint, request
from src.controllers.profileController import createProfile, updateProfile, getProfile

profileBlueprint = Blueprint('profile', __name__)

@profileBlueprint.route('/add', methods=['POST'])
def addProfile():
    data = request.get_json()
    return createProfile(data)

@profileBlueprint.route('/update', methods=['PUT'])
def putProfile():
    data = request.get_json()
    return updateProfile(data)

@profileBlueprint.route('/profile', methods=['POST'])
def viewProfile():
    data = request.get_json()
    return getProfile(data)

