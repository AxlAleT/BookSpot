from flask import Blueprint, jsonify
from app import db
from modelos.modelo_movimiento import Movimiento
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

bp_reporte = Blueprint('bp_reporte', __name__, url_prefix='/reporte')

@bp_reporte.route('/movimientos', methods=['GET'])
def reporte_movimientos():
    movimientos = Movimiento.query.all()
    filename = f"movimientos_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = f"static/{filename}"
    
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



