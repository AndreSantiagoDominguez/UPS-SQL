from flask import Blueprint, request
from src.controllers.contributionsController import createContribution, getDonor

contributiosBlueprint = Blueprint('contributions', __name__)

@contributiosBlueprint.route('/add', methods=['POST'])
def addContribution():
    data = request.get_json()
    return createContribution(data)

@contributiosBlueprint.route('/', methods=['GET'])
def allContibutions():
    return getDonor()