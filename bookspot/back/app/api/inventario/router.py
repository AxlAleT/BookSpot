from flask import Blueprint, request, jsonify
from app import db
from app.compartido.modelos.modelo_libro import Libro
from app.compartido.modelos.modelo_movimiento import Movimiento, DetallesMovimiento, TipoMovimiento
from app.compartido.excepciones.excepciones_libro import InvalidRequestException, BookNotFoundException
import datetime
from .schemas import AddLibroSchema, EditLibroSchema, SearchLibroSchema


inventario_bp = Blueprint('inventario', __name__)


# Definir el endpoint para obtener libros
@inventario_bp.route('/obtener_libros/', methods=['GET'])
def obtener_libros():
    numero = request.args.get('numero', type=int)
    
    if numero is None or numero < 0 or numero % 100 != 0:
        raise InvalidRequestException("El número debe ser un múltiplo de 100 y no negativo.")

    try:
        # Calcular el offset basado en el número recibido
        offset = numero

        # Obtener 100 libros a partir del offset
        libros = Libro.query.offset(offset).limit(100).all()

        # Convertir los libros a diccionarios
        libros_dict = [libro.to_dict() for libro in libros]

        return jsonify(libros_dict), 200
        
    except InvalidRequestException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Definir el endpoint para agregar libro
@inventario_bp.route('/agregar_libro/', methods=['POST'])
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


# Endpoint para editar libro
@inventario_bp.route('/editar_libro/', methods=['PUT'])
def editar_libro():
    request_data = request.json
    
    if request_data is None:
        raise InvalidRequestException("Solicitud inválida, no se proporcionó JSON.")
    
    try:
        # Validar la solicitud
        validate_edit_libro_request(request_data)

        libro_id = request_data.get('id')
        titulo = request_data.get('titulo')
        precio = request_data.get('precio')
        available_quantity = request_data.get('available_quantity')
        
        # Buscar el libro por ID
        libro = Libro.query.get(libro_id)
        
        if not libro:
            raise BookNotFoundException(libro_id)

        # Actualizar los campos del libro
        libro.titulo = titulo
        libro.precio = precio
        libro.available_quantity = available_quantity

        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return jsonify({"message": "Libro editado exitosamente.", "libro": libro.to_dict()}), 200
        
    except (InvalidRequestException, BookNotFoundException) as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error general
        return jsonify({"error": str(e)}), 500



# Endpoint para buscar libros por palabra clave en el título
@inventario_bp.route('/buscar_libro/', methods=['GET'])
def buscar_libro():
    keyword = request.args.get('keyword', type=str)
    
    if not keyword:
        raise InvalidRequestException("Solicitud inválida, no se proporcionó una palabra clave.")
    
    try:
        # Validar la solicitud
        validate_search_libro_request({'keyword': keyword})

        # Buscar libros cuyo título contenga la palabra clave
        libros = Libro.query.filter(Libro.titulo.ilike(f'%{keyword}%')).all()

        # Convertir los libros a diccionarios
        libros_dict = [libro.to_dict() for libro in libros]

        return jsonify(libros_dict), 200
        
    except InvalidRequestException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# Función para validar la solicitud de edición de libro
def validate_edit_libro_request(request_data):
    try:
        EditLibroSchema().load(request_data)
    except Exception as e:
        raise InvalidRequestException(str(e))

# Función para validar la solicitud
def validate_add_libro_request(request_data):
    try:
        AddLibroSchema().load(request_data)
    except Exception as e:
        raise InvalidRequestException(str(e))
    
# Función para validar la solicitud de búsqueda de libro
def validate_search_libro_request(request_data):
    try:
        SearchLibroSchema().load(request_data)
    except Exception as e:
        raise InvalidRequestException(str(e))