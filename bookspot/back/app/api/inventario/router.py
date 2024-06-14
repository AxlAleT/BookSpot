from flask import Blueprint, request, jsonify
from app import db
from app.compartido.modelos.modelo_libro import Libro
from app.compartido.modelos.modelo_movimiento import Movimiento, DetallesMovimiento, TipoMovimiento
from app.compartido.excepciones.excepciones_libro import InvalidRequestException, BookNotFoundException
import datetime
from .schemas import Schema

# Definir el Blueprint
libros_bp = Blueprint('libros', __name__)

# Definir el endpoint para agregar libro
@libros_bp.route('/agregar_libro/', methods=['POST'])
def agregar_libro():
    request_data = request.json
    
    if request_data is None:
        raise InvalidRequestException()
    
    try:
        # Validar la solicitud
        validate_add_libro_request(request_data)

        titulo = request_data.get('titulo')
        precio = request_data.get('precio')
        cantidad = request_data.get('cantidad')
        
        # Buscar si el libro ya existe
        libro = Libro.query.filter_by(titulo=titulo).first()
        
        if libro:
            # Si el libro existe, actualizar la cantidad
            libro.available_quantity += cantidad
        else:
            # Si el libro no existe, crear una nueva entrada
            libro = Libro(titulo=titulo, precio=precio, available_quantity=cantidad)
            db.session.add(libro)

        # Crear una nueva entrada en la tabla Movimiento
        tipo_movimiento_rli = TipoMovimiento.query.filter_by(nombre='RLI').first()
        if not tipo_movimiento_rli:
            raise InvalidRequestException("Tipo de movimiento no encontrado")
        
        nuevo_movimiento = Movimiento(
            id_tipo_movimiento=tipo_movimiento_rli.id_tipo_movimiento,
            fecha_hora=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()  # Commit para obtener el ID del movimiento
        
        # Obtener el ID del movimiento recién creado
        id_movimiento = nuevo_movimiento.id_movimiento

        # Crear una entrada en la tabla DetallesMovimiento
        nuevo_detalle = DetallesMovimiento(
            id_movimiento=id_movimiento,
            id_libro=libro.id,
            cantidad=cantidad
        )
        db.session.add(nuevo_detalle)

        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return jsonify({"message": "Libro agregado exitosamente.", "libro": libro.to_dict()}), 200
        
    except InvalidRequestException as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error general
        return jsonify({"error": str(e)}), 500

# Función para validar la solicitud
def validate_add_libro_request(request_data):
    try:
        Schema.AddLibroSchema().load(request_data)
    except Exception as e:
        raise InvalidRequestException(str(e))

# Asegurarse de que el Blueprint esté registrado en la aplicación principal
# from app import app
# app.register_blueprint(libros_bp, url_prefix='/api')
