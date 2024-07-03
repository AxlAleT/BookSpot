from flask import Blueprint, current_app
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from modelos.modelo_movimiento import Movimiento  # Asegúrate de ajustar los imports según la estructura de tu proyecto

reportes_blueprint = Blueprint('reportes', __name__, url_prefix='/reportes')

def get_next_report_number():
    report_folder = os.path.join(current_app.root_path, 'static')
    reports = [f for f in os.listdir(report_folder) if f.startswith('reportemovimiento') and f.endswith('.pdf')]
    max_number = 0
    for report in reports:
        parts = report.replace('reportemovimiento', '').replace('.pdf', '')
        if parts.isdigit():
            number = int(parts)
            if number > max_number:
                max_number = number
    return max_number + 1

@reportes_blueprint.route('/movimientos_pdf', methods=['GET'])
def generar_reporte_movimientos():
    report_number = get_next_report_number()
    pdf_filename = f"reportemovimiento{report_number}.pdf"
    pdf_path = os.path.join(current_app.root_path, 'static', pdf_filename)

    c = canvas.Canvas(pdf_path)
    c.drawString(100, 800, "Reporte de Movimientos")
    
    y = 780
    for movimiento in movimientos:
        c.drawString(100, y, f"ID: {movimiento.id_movimiento}, Tipo: {movimiento.tipo_movimiento.nombre}, Fecha: {movimiento.fecha_hora}")
        y -= 20
        for detalle in movimiento.detalles:
            c.drawString(120, y, f"Libro ID: {detalle.id_libro}, Cantidad: {detalle.cantidad}")
            y -= 20

    c.save()
    return {'filename': pdf_filename}
