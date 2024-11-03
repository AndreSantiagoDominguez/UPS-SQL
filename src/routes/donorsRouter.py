from flask import Blueprint, request
from src.controllers.donorsController import createDonor, updateDonor, login, delete

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
