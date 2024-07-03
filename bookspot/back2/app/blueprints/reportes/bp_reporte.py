from flask import Blueprint, jsonify, current_app
from app import db
from app.modelos.modelo_movimiento import Movimiento
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

reporte_bp = Blueprint('bp_reporte', __name__, url_prefix='/reporte')

@reporte_bp.route('/movimientos', methods=['GET'])
def reporte_movimientos():
    try:
        current_app.logger.debug("Fetching movements...")
        movimientos = Movimiento.query.all()
        
        if not movimientos:
            current_app.logger.debug("No movements found!")
            return jsonify({"message": "No hay movimientos por el momento"}), 404

        # Verifica y crea la carpeta pdfs si no existe
        pdf_folder = os.path.join(current_app.root_path, 'pdfs')
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
            current_app.logger.debug(f"Created folder: {pdf_folder}")

        filename = f"movimientos_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        path = os.path.join(pdf_folder, filename)
        current_app.logger.debug(f"Saving PDF at {path}...")
        
        # Crear el PDF
        c = canvas.Canvas(path, pagesize=letter)
        width, height = letter  # keep for later
        
        c.drawString(100, height - 50, "Reporte de Movimientos")
        y = height - 70
        
        for movimiento in movimientos:
            fecha = movimiento.fecha_hora.strftime("%Y-%m-%d %H:%M:%S") if movimiento.fecha_hora else "Sin Fecha"
            tipo_movimiento = movimiento.tipo_movimiento.nombre if movimiento.tipo_movimiento else "Sin Tipo"
            c.drawString(50, y, f"ID: {movimiento.id_movimiento} - Fecha: {fecha} - Tipo: {tipo_movimiento}")
            y -= 20
        
        c.save()

        return jsonify({"message": "PDF generado", "filename": filename})
    except Exception as e:
        current_app.logger.error(f"Error generating PDF: {e}")
        return jsonify({"error": str(e)}), 500

