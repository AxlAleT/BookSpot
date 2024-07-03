from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from marshmallow import ValidationError

# Asegúrate de que la importación sea correcta
from schema_reporte import EntradaDatosSchema

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/ingresar_datos', methods=['POST'])
def ingresar_datos_y_generar_reporte():
    try:
        # Validar la solicitud con el esquema de EntradaDatosSchema
        datos = EntradaDatosSchema().load(request.get_json())  # Asegúrate de usar get_json() para obtener el JSON de la solicitud
        movimientos = datos['movimientos']
        ventas = datos['ventas']

        # Generación del reporte PDF
        report_path = os.path.join(os.path.dirname(__file__), f"reporte_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        c = canvas.Canvas(report_path, pagesize=letter)
        width, height = letter

        y = height - 30
        c.drawString(30, y, f'Reporte generado el: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        y -= 20

        # Detalles de los movimientos
        c.drawString(30, y, 'Movimientos:')
        y -= 20
        for movimiento in movimientos:
            c.drawString(30, y, f'Tipo: {movimiento["id_tipo_movimiento"]}, Fecha: {movimiento["fecha_hora"]}, Cantidad: {movimiento["cantidad"]}')
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 30

        # Detalles de las ventas
        y -= 20
        c.drawString(30, y, 'Ventas:')
        y -= 20
        for venta in ventas:
            c.drawString(30, y, f'Libro ID: {venta["id_libro"]}, Cantidad: {venta["cantidad"]}, Precio: ${venta["precio_venta"]}, Fecha: {venta["fecha_venta"]}')
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 30

        c.save()
        return jsonify({"message": f"Datos ingresados y reporte generado correctamente. Guardado en {report_path}"}), 200
        
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400