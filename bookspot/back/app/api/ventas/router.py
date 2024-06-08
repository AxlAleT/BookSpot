from flask import Blueprint, request, jsonify
from .schemas import LibroResponseSchema, VentaRequestSchema
from app.compartido.modelos.modelo_libro import Libro
from app import db
from app.compartido.excepciones.excepciones_libro import BookNotFoundException, NotEnoughStockException, InvalidRequestException

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/get_libro/', methods=['POST'])
def get_libro():
    request_data = request.json
    
    if request_data is None:
        raise InvalidRequestException()

    try:
        # Validar la solicitud
        validate_request(request_data)
        # Obtener el ID del libro y la cantidad del JSON
        items = request_data.get('items')
        item = items[0]
        libro_id = item.get('id_libro')
        cantidad = item.get('cantidad')

        # Verificar si el libro existe y hay suficiente stock
        libro = Libro.query.get(libro_id)
        if libro is None:
            raise BookNotFoundException(libro_id)
        if libro.available_quantity < cantidad:
            raise NotEnoughStockException(libro_id, cantidad, libro.available_quantity)
        
        # Preparar la respuesta
        libro_response = {
            'titulo': libro.titulo,
            'id_libro': libro.id,
            'precio': libro.precio,
            'cantidad': cantidad
        }
        return jsonify(LibroResponseSchema().dump(libro_response))
    except (InvalidRequestException, BookNotFoundException, NotEnoughStockException) as e:
        return e.response

def validate_request(request_data):
    try:
        VentaRequestSchema().load(request_data)
    except:
        raise InvalidRequestException()
