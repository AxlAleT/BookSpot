from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app import db
from app.compartido.modelos.modelo_usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/', methods=['POST'])
def login():
    request_data = request.json
    correo_electronico = request_data.get('correo_electronico')
    password = request_data.get('password')

    if not correo_electronico or not password:
        return jsonify({"error": "Correo electrónico y contraseña son requeridos"}), 400

    usuario = Usuario.query.filter_by(correo_electronico=correo_electronico).first()

    if usuario is None or not usuario.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Aquí deberías generar y devolver un token de autenticación o una sesión, según tu lógica de autenticación.
    # Por simplicidad, solo devolveremos un mensaje de éxito.
    return jsonify({"message": "Inicio de sesión exitoso"}), 200