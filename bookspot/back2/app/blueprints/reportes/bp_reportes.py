from flask import Blueprint, request, jsonify, send_file
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from marshmallow import ValidationError

# Importación ajustada
from schema_reporte import EntradaDatosSchema

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/ingresar_datos', methods=['POST'])
def ingresar_datos_y_generar_reporte():
    try:
        # Validar la solicitud con el esquema de EntradaDatosSchema
        datos = EntradaDatosSchema().load(request.get_json())
        movimientos = datos['movimientos']
        ventas = datos['ventas']

        # Filtrar movimientos por el nombre del empleado
        nombre_empleado = request.args.get('nombre_empleado')
        movimientos_filtrados = [m for m in movimientos if m['nombre_empleado'] == nombre_empleado]

        # Generación del reporte PDF
        report_path = os.path.join(os.path.dirname(__file__), f"reporte_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        c = canvas.Canvas(report_path, pagesize=letter)
        width, height = letter

        y = height - 30
        c.drawString(30, y, f'Reporte generado el: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        y -= 20

        # Detalles de los movimientos filtrados
        c.drawString(30, y, 'Movimientos:')
        y -= 20
        for movimiento in movimientos_filtrados:
            c.drawString(30, y, f'Tipo: {movimiento["id_tipo_movimiento"]}, Empleado: {movimiento["nombre_empleado"]}, Fecha: {movimiento["fecha_hora"]}, Cantidad: {movimiento["cantidad"]}')
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

        # Enviar el archivo PDF generado para abrirlo en una nueva ventana del navegador
        return send_file(report_path, as_attachment=True, attachment_filename=os.path.basename(report_path))
        
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
