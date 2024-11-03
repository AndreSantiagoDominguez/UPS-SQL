from flask import Blueprint, request
from src.controllers.doneesController import createDonee, updateDonee, login, getDonee, delete

doneesBlueprint = Blueprint('donees', __name__)

@doneesBlueprint.route('/add', methods=['POST'])
def addDonee():
    data = request.get_json()
    return createDonee(data)

@doneesBlueprint.route('/update/<int:id_donee>', methods=['PUT'])
def putDonee(id_donee):
    data = request.get_json()
    return updateDonee(id_donee, data)

@doneesBlueprint.route('/login', methods=['POST'])
def loginR():
    data = request.get_json()
    return login(data)

@doneesBlueprint.route('/profile', methods=['GET'])
def viewProfile():
    return getDonee()

@doneesBlueprint.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return delete()
