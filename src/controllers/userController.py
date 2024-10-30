from flask import jsonify
from src.models.user import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def crear_usuario(data):
    # if not nombre or not email or not password:
    #     return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    # if User.query.filter_by(email=email).first():
    #     return jsonify({"mensaje": "El email ya está registrado"}), 400 

    newUser = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['credentials']['email'],
        password=data['credentials']['password'],
        state=data['address']['state'],
        locality=data['address']['locality'],
        distrit=data['address']['distrit']
    )

    db.session.add(newUser)
    db.session.commit()
    return jsonify({
        "mensaje": "Usuario creado con bcrypt",
        "id": newUser.id_user,
        "nombre": newUser.first_name,
        "email": newUser.email
    }), 201

# def crear_usuario_base(data):
#     nombre = data.get('nombre')
#     email = data.get('email')
#     password = data.get('password')
#     if not nombre or not email or not password:
#         return jsonify({"mensaje": "Faltan campos obligatorios"}), 400
#     if User.query.filter_by(email=email).first():
#         return jsonify({"mensaje": "El email ya está registrado"}), 400
#     nuevo_usuario = User(nombre=nombre, email=email, password=password)
#     db.session.add(nuevo_usuario)
#     db.session.commit()
#     return jsonify({
#         "mensaje": "Usuario creado sin bcrypt",
#         "id": nuevo_usuario.id,
#         "nombre": nuevo_usuario.nombre,
#         "email": nuevo_usuario.email
#     }), 201

# def login_usuario(data):
#     email = data.get('email')
#     password = data.get('password')
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({"mensaje": "Credenciales inválidas"}), 401
#     if not user.check_password(password):
#         return jsonify({"mensaje": "Credenciales inválidas"}), 401
#     access_token = create_access_token(identity=user.id)
#     return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200

# @jwt_required()
# def obtener_usuario():
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"mensaje": "Usuario no encontrado"}), 404
#     return jsonify({
#         "id": user.id,
#         "nombre": user.nombre,
#         "email": user.email
#     }), 200

# @jwt_required()
# def eliminar_usuario(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"mensaje": "Usuario no encontrado"}), 404
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({"mensaje": "Usuario eliminado"}), 200
