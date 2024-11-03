from flask import Blueprint, request
from src.controllers.donorsController import createDonor, updateDonor, login, delete

donorsBlueprint = Blueprint('donors', __name__)

@donorsBlueprint.route('/add', methods=['POST'])
def addDonor():
    data = request.get_json()
    return createDonor(data)

@donorsBlueprint.route('/update/<int:id_donor>', methods=['PUT'])
def putDonor(id_donor):
    data = request.get_json()
    return updateDonor(id_donor, data)

@donorsBlueprint.route('/login', methods=['POST'])
def loginR():
    data = request.get_json()
    return login(data)

@donorsBlueprint.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return delete()
