from functools import wraps
from flask import session, jsonify

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