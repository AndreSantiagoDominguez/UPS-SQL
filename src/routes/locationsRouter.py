from flask import Blueprint
from src.controllers.locationsController import getLocations, getDetailsLocation

locationsBlueprint = Blueprint('locations', __name__)

@locationsBlueprint.route('/', methods=['GET'])
def allLocations():
    return getLocations()

@locationsBlueprint.route('/<int:id_bank>', methods=['GET'])
def getLocation(id_bank):
    return getDetailsLocation(id_bank)