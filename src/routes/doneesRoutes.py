from flask import Blueprint, request
from src.controllers.doneesController import createDonee, updateDonee, login
from flask_jwt_extended import JWTManager

doneesBlueprint = Blueprint('donees', __name__)

@doneesBlueprint.route('/add', methods=['POST'])
def addDonee():
    data = request.get_json()
    return createDonee(data)

@doneesBlueprint.route('/update/<int:id_donee>', methods=['PUT'])
def putDonee(id_donee):
    data = request.get_json()
    return updateDonee(id_donee, data)

# @usuario_blueprint.route('/users_base', methods=['POST'])
# def crear_usuario_base_ruta():
#     data = request.get_json()
#     return crear_usuario_base(data)

@doneesBlueprint.route('/login', methods=['POST'])
def login_ruta():
    data = request.get_json()
    return login(data)

# @usuario_blueprint.route('/profile', methods=['GET'])
# def obtener_usuario_ruta():
#     return obtener_usuario()

# @usuario_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
# def eliminar_usuario_ruta(user_id):
#     return eliminar_usuario(user_id)
