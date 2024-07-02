from flask import Blueprint, request, jsonify
from app import db
from app.modelos.modelo_apartado import Apartado, DetallesApartado
from app.modelos.modelo_movimiento import Movimiento, TipoMovimiento, DetallesMovimiento
from app.modelos.modelo_libro import Libro
from app.modelos.modelo_venta import Venta, DetallesVenta
from .schema_apartado import ApartadoRequestSchema, ApartadoResponseSchema
from app.excepciones.excepciones_libro import InvalidRequestException, BookNotFoundException, NotEnoughStockException
from config import negocioConfig as Config
import datetime
from app.auth.auth import requiere_vendedor

apartados_bp = Blueprint('apartados', __name__)

@apartados_bp.route('/crear_apartado/', methods=['POST'])
@requiere_vendedor
def crear_apartado():
    request_data = request.json
    
    if request_data is None:
        raise InvalidRequestException()

    try:
        # Validar la solicitud
        ApartadoRequestSchema().load(request_data)
        
        # Obtener datos de la solicitud
        id_usuario = request_data.get('id_usuario')
        fecha_limite = request_data.get('fecha_limite')
        monto = request_data.get('monto')
        nombre_acreedor = request_data.get('nombre_acreedor')
        items = request_data.get('items')

        # Verificar la disponibilidad de cada libro
        for item in items:
            id_libro = item.get('id_libro')
            cantidad = item.get('cantidad')

            # Obtener el libro
            libro = Libro.query.get(id_libro)
            if libro is None:
                raise BookNotFoundException(id_libro)

            # Obtener las cantidades apartadas de este libro
            apartados_existentes = db.session.query(db.func.sum(DetallesApartado.cantidad)).filter(DetallesApartado.id_libro == id_libro).scalar() or 0
            
            # Calcular el total disponible y el total apartado
            total_disponible = libro.available_quantity + apartados_existentes
            total_apartado = apartados_existentes + cantidad

            # Verificar si se excede el porcentaje permitido
            if total_apartado / total_disponible > Config.APARTADO_PORCENTAJE:
                return jsonify({"error": f"Cannot create apartado, exceeds {Config.APARTADO_PORCENTAJE * 100}% of total available for book id {id_libro}"}), 400

        # Crear una nueva entrada en la tabla Apartado
        nuevo_apartado = Apartado(
            id_usuario=id_usuario,
            fecha_limite=fecha_limite,
            monto=monto,
            nombre_acreedor=nombre_acreedor
        )
        db.session.add(nuevo_apartado)
        db.session.commit()  # Commit para obtener el ID del apartado

        # Obtener el ID del apartado recién creado
        id_apartado = nuevo_apartado.id_apartado

        # Crear una nueva entrada en la tabla Movimiento
        tipo_movimiento_apv = TipoMovimiento.query.filter_by(nombre='APV').first()
        if not tipo_movimiento_apv:
            raise InvalidRequestException()

        nuevo_movimiento = Movimiento(
            id_tipo_movimiento=tipo_movimiento_apv.id_tipo_movimiento,
            fecha_hora=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()  # Commit para obtener el ID del movimiento

        # Obtener el ID del movimiento recién creado
        id_movimiento = nuevo_movimiento.id_movimiento

        # Procesar los detalles del apartado y actualizar el inventario de libros
        for item in items:
            id_libro = item.get('id_libro')
            cantidad = item.get('cantidad')
            precio_apartado = item.get('precio_apartado')

            # Actualizar la cantidad disponible del libro
            libro.available_quantity -= cantidad

            # Crear una entrada en la tabla DetallesApartado
            nuevo_detalle_apartado = DetallesApartado(
                id_apartado=id_apartado,
                id_libro=id_libro,
                cantidad=cantidad,
                precio_apartado=precio_apartado
            )
            db.session.add(nuevo_detalle_apartado)

            # Crear una entrada en la tabla DetallesMovimiento
            nuevo_detalle_movimiento = DetallesMovimiento(
                id_movimiento=id_movimiento,
                id_libro=id_libro,
                cantidad=cantidad
            )
            db.session.add(nuevo_detalle_movimiento)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return jsonify(ApartadoResponseSchema().dump(nuevo_apartado)), 200

    except (InvalidRequestException, BookNotFoundException, NotEnoughStockException) as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return e.response, 400
    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error general
        return jsonify({"error": str(e)}), 500

def validate_request(request_data):
    try:
        ApartadoRequestSchema().load(request_data)
    except:
        raise InvalidRequestException()


@apartados_bp.route('/concretar_venta_apartado/', methods=['POST'])
@requiere_vendedor
def concretar_venta_apartado():
    request_data = request.json

    if request_data is None:
        raise InvalidRequestException()

    try:
        id_apartado = request_data.get('id_apartado')
        if id_apartado is None:
            raise InvalidRequestException("id_apartado is required")

        # Obtener el apartado
        apartado = Apartado.query.get(id_apartado)
        if apartado is None:
            raise InvalidRequestException(f"Apartado with id {id_apartado} not found")

        # Crear una nueva entrada en la tabla Movimiento
        tipo_movimiento_acv = TipoMovimiento.query.filter_by(nombre='ACV').first()
        if not tipo_movimiento_acv:
            raise InvalidRequestException("Tipo de movimiento ACV no encontrado")

        nuevo_movimiento = Movimiento(
            id_tipo_movimiento=tipo_movimiento_acv.id_tipo_movimiento,
            fecha_hora=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()  # Commit para obtener el ID del movimiento

        # Obtener el ID del movimiento recién creado
        id_movimiento = nuevo_movimiento.id_movimiento

        # Crear una nueva entrada en la tabla Venta
        nueva_venta = Venta(
            fecha_venta=datetime.datetime.now(datetime.timezone.utc),
            id_usuario=apartado.id_usuario,
            monto=apartado.monto
        )
        db.session.add(nueva_venta)
        db.session.commit()  # Commit para obtener el ID de la venta

        # Obtener el ID de la venta recién creada
        id_venta = nueva_venta.id_venta

        # Crear entradas en la tabla DetallesVenta
        for detalle_apartado in apartado.detalles:
            nuevo_detalle_venta = DetallesVenta(
                id_venta=id_venta,
                id_libro=detalle_apartado.id_libro,
                cantidad=detalle_apartado.cantidad,
                precio_venta=detalle_apartado.precio_apartado
            )
            db.session.add(nuevo_detalle_venta)

            # Crear una entrada en la tabla DetallesMovimiento
            nuevo_detalle_movimiento = DetallesMovimiento(
                id_movimiento=id_movimiento,
                id_libro=detalle_apartado.id_libro,
                cantidad=detalle_apartado.cantidad
            )
            db.session.add(nuevo_detalle_movimiento)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Venta concretada exitosamente."}), 200

    except (InvalidRequestException, BookNotFoundException, NotEnoughStockException) as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return e.response, 400
    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error general
        return jsonify({"error": str(e)}), 500


@apartados_bp.route('/cancelar_apartado/', methods=['DELETE'])
@requiere_vendedor
def cancelar_apartado():
    request_data = request.json

    if request_data is None:
        return jsonify({"error": "Request data is required"}), 400

    try:
        id_apartado = request_data.get('id_apartado')
        if id_apartado is None:
            return jsonify({"error": "id_apartado is required"}), 400

        # Obtener el apartado
        apartado = Apartado.query.get(id_apartado)
        if apartado is None:
            return jsonify({"error": f"Apartado with id {id_apartado} not found"}), 404

        # Crear una nueva entrada en la tabla Movimiento
        tipo_movimiento_ela = TipoMovimiento.query.filter_by(nombre='ELA').first()
        if not tipo_movimiento_ela:
            return jsonify({"error": "Tipo de movimiento ELA no encontrado"}), 400

        nuevo_movimiento = Movimiento(
            id_tipo_movimiento=tipo_movimiento_ela.id_tipo_movimiento,
            fecha_hora=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()  # Commit para obtener el ID del movimiento

        # Obtener el ID del movimiento recién creado
        id_movimiento = nuevo_movimiento.id_movimiento

        # Reestablecer las cantidades de los libros y eliminar los detalles del apartado
        for detalle_apartado in apartado.detalles:
            libro = Libro.query.get(detalle_apartado.id_libro)
            if libro:
                libro.available_quantity += detalle_apartado.cantidad

            # Crear una entrada en la tabla DetallesMovimiento
            nuevo_detalle_movimiento = DetallesMovimiento(
                id_movimiento=id_movimiento,
                id_libro=detalle_apartado.id_libro,
                cantidad=-detalle_apartado.cantidad  # Cantidad negativa para indicar restablecimiento
            )
            db.session.add(nuevo_detalle_movimiento)

        # Eliminar los detalles del apartado
        DetallesApartado.query.filter_by(id_apartado=id_apartado).delete()
        # Eliminar el apartado
        db.session.delete(apartado)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Apartado cancelado exitosamente."}), 200

    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return jsonify({"error": str(e)}), 500
    

@apartados_bp.route('/modificar_apartado/', methods=['PATCH'])
@requiere_vendedor
def modificar_apartado():
    request_data = request.json

    if request_data is None:
        return jsonify({"error": "Request data is required"}), 400

    try:
        # Obtener datos del apartado
        id_apartado = request_data.get('id_apartado')
        id_usuario = request_data.get('id_usuario')
        fecha_limite = request_data.get('fecha_limite')
        monto = request_data.get('monto')
        nombre_acreedor = request_data.get('nombre_acreedor')
        detalles = request_data.get('detalles')

        if not all([id_apartado, id_usuario, fecha_limite, monto, nombre_acreedor, detalles]):
            return jsonify({"error": "All fields are required"}), 400

        # Buscar el apartado
        apartado = Apartado.query.get(id_apartado)
        if apartado is None:
            return jsonify({"error": f"Apartado with id {id_apartado} not found"}), 404

        # Actualizar información del apartado
        apartado.id_usuario = id_usuario
        apartado.fecha_limite = datetime.datetime.fromisoformat(fecha_limite)
        apartado.monto = monto
        apartado.nombre_acreedor = nombre_acreedor

        # Eliminar los detalles existentes del apartado
        DetallesApartado.query.filter_by(id_apartado=id_apartado).delete()

        # Agregar los nuevos detalles del apartado
        for detalle in detalles:
            nuevo_detalle = DetallesApartado(
                id_apartado=id_apartado,
                id_libro=detalle['id_libro'],
                cantidad=detalle['cantidad'],
                precio_apartado=detalle['precio_apartado']
            )
            db.session.add(nuevo_detalle)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Apartado modificado exitosamente."}), 200

    except Exception as e:
        db.session.rollback()  # Deshacer cualquier cambio en caso de error
        return jsonify({"error": str(e)}), 500