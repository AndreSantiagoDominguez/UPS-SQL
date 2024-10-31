from flask import Blueprint, request
from src.controllers.doneesController import createDonee
from flask_jwt_extended import JWTManager

doneesBlueprint = Blueprint('donees', __name__)

@doneesBlueprint.route('/add', methods=['POST'])
def addDonee():
    data = request.get_json()
    return createDonee(data)

# @usuario_blueprint.route('/users_base', methods=['POST'])
# def crear_usuario_base_ruta():
#     data = request.get_json()
#     return crear_usuario_base(data)

# @usuario_blueprint.route('/login', methods=['POST'])
# def login_ruta():
#     data = request.get_json()
#     return login_usuario(data)

# @usuario_blueprint.route('/profile', methods=['GET'])
# def obtener_usuario_ruta():
#     return obtener_usuario()

# @usuario_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
# def eliminar_usuario_ruta(user_id):
#     return eliminar_usuario(user_id)
