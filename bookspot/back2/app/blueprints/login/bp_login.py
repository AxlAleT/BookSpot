from flask import Blueprint, request, jsonify, session
from app import db
from app.modelos.modelo_usuario import Usuario
from .schema_login import InicioSesionSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/', methods=['POST'])
def iniciar_sesion():
    request_data = request.json
    schema = InicioSesionSchema()
    errors = schema.validate(request_data)
    if errors:
        return jsonify(errors), 400

    correo_electronico = request_data.get('correo_electronico')
    password = request_data.get('password')

    usuario = Usuario.query.filter_by(correo_electronico=correo_electronico).first()

    if usuario and usuario.check_password(password):  # Usar el método check_password del modelo Usuario
        # Establecer el estado de la sesión aquí
        session['usuario_id'] = usuario.id
        session['grupo'] = usuario.grupo.nombre  # Acceder al nombre del grupo a través de la relación

        return jsonify({"mensaje": "Inicio de sesion exitoso", "usuario": usuario.to_dict()}), 200
    else:
        return jsonify({"error": "Correo electronico o contrasena incorrectos"}), 401


@auth_bp.route('/logout/', methods=['POST'])
def cerrar_sesion():
    # Eliminar los datos de la sesión
    session.pop('usuario_id', None)
    session.pop('grupo', None)
    return jsonify({"mensaje": "Sesión cerrada exitosamente"}), 200