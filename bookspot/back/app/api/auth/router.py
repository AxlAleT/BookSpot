from flask import Blueprint, request, jsonify, session  
from app import db
from app.compartido.modelos.modelo_usuario import Usuario
from .schemas import InicioSesionSchema
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/', methods=['POST'])
def iniciar_sesion():
    print("Iniciar sesion")
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

        return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario.to_dict()}), 200
    else:
        return jsonify({"error": "Correo electrónico o contraseña incorrectos"}), 401
    

def requiere_grupo(grupo_requerido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'grupo' not in session:
                return jsonify({"error": "Acceso no autorizado. Por favor, inicie sesión."}), 403
            if session['grupo'] != grupo_requerido:
                return jsonify({"error": "Acceso no autorizado para este grupo."}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Decoradores específicos para cada grupo
requiere_admin = requiere_grupo('admin')
requiere_vendedor = requiere_grupo('vendedor')
requiere_almacenista = requiere_grupo('almacenista')