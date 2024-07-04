from flask import Blueprint, request, jsonify, session
from .schema_ventas import LibroResponseSchema, VentaRequestSchema
from app.modelos.modelo_libro import Libro
from app import db
import datetime
from app.modelos.modelo_movimiento import Movimiento, DetallesMovimiento, TipoMovimiento
from app.excepciones.excepciones_libro import InvalidRequestException, BookNotFoundException, NotEnoughStockException
from app.modelos.modelo_venta import Venta, DetallesVenta
from app.modelos.modelo_metodo_pago import MetodoPago
from app.auth.auth import requiere_vendedor
from app.blueprints.reportes.bp_reportes import generar_reporte_ventas

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/get_libro/', methods=['POST'])
@requiere_vendedor
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
    

@ventas_bp.route('/completar/', methods=['PATCH'])
@requiere_vendedor
def completar():
    request_data = request.json
    
    if request_data is None:
        raise InvalidRequestException()

    try:
        # Validar la solicitud
        validate_request(request_data)
        
        # Obtener los elementos del pedido
        items = request_data.get('items')
        metodo_pago = request_data.get('metodo_pago')

        # Validar el método de pago
        metodo_pago_obj = MetodoPago.query.filter_by(nombre=metodo_pago).first()
        if not metodo_pago_obj:
            raise InvalidRequestException(f"Método de pago {metodo_pago} no es válido")

        # Crear una nueva entrada en la tabla Movimiento
        tipo_movimiento_vpv = TipoMovimiento.query.filter_by(nombre='VPV').first()
        if not tipo_movimiento_vpv:
            raise InvalidRequestException()

        nuevo_movimiento = Movimiento(
            id_tipo_movimiento=tipo_movimiento_vpv.id_tipo_movimiento,
            fecha_hora=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()  # Commit para obtener el ID del movimiento

        # Obtener el ID del movimiento recién creado
        id_movimiento = nuevo_movimiento.id_movimiento

        # Calcular el monto total de la venta
        monto_total = 0

        for item in items:
            libro_id = item.get('id_libro')
            cantidad = item.get('cantidad')

            # Verificar si el libro existe y hay suficiente stock
            libro = Libro.query.get(libro_id)
            if libro is None:
                raise BookNotFoundException(libro_id)
            if libro.available_quantity < cantidad:
                raise NotEnoughStockException(libro_id, cantidad, libro.available_quantity)
            
            # Actualizar la cantidad disponible del libro
            libro.available_quantity -= cantidad

            # Crear una entrada en la tabla DetallesMovimiento
            nuevo_detalle = DetallesMovimiento(
                id_movimiento=id_movimiento,
                id_libro=libro_id,
                cantidad=cantidad
            )
            db.session.add(nuevo_detalle)

            # Actualizar el monto total
            monto_total += libro.precio * cantidad

        # Crear una nueva entrada en la tabla Venta
        nueva_venta = Venta(
            fecha_venta=datetime.datetime.now(datetime.timezone.utc),
            id_usuario = session.get('usuario_id'),
            monto=monto_total
        )
        db.session.add(nueva_venta)
        db.session.commit()  # Commit para obtener el ID de la venta

        # Obtener el ID de la venta recién creada
        id_venta = nueva_venta.id_venta

        # Crear entradas en la tabla DetallesVenta
        for item in items:
            libro_id = item.get('id_libro')
            cantidad = item.get('cantidad')
            precio_venta = Libro.query.get(libro_id).precio

            nuevo_detalle_venta = DetallesVenta(
                id_venta=id_venta,
                id_libro=libro_id,
                cantidad=cantidad,
                precio_venta=precio_venta
            )
            db.session.add(nuevo_detalle_venta)

        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        
        
        
        return jsonify({"message": "Venta completada exitosamente."}), 200
        
    except (InvalidRequestException, BookNotFoundException, NotEnoughStockException) as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return e.response, 400
    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error general
        return jsonify({"error": str(e)}), 500


def validate_request(request_data):
    try:
        VentaRequestSchema().load(request_data)
    except:
        raise InvalidRequestException()