from flask import Blueprint, jsonify, current_app
from app import db
from app.modelos.modelo_venta import Venta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

reporte_bp = Blueprint('bp_reporte', __name__, url_prefix='/reporte')

def generar_reporte_ventas(id_venta):
    venta = Venta.query.get(id_venta)
    if not venta:
        current_app.logger.debug("Venta no encontrada")
        return None

    pdf_folder = os.path.join(current_app.root_path, 'pdfs')
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        current_app.logger.debug(f"Created folder: {pdf_folder}")

    filename = f"venta_{venta.id_venta}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = os.path.join(pdf_folder, filename)
    current_app.logger.debug(f"Saving PDF at {path}...")

    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 50, "Reporte de Venta Individual")
    y = height - 70

    fecha = venta.fecha_venta.strftime("%Y-%m-%d %H:%M:%S") if venta.fecha_venta else "Sin Fecha"
    detalles = "\n".join([f"Libro ID: {detalle.libro_id}, Cantidad: {detalle.cantidad}, Precio: ${detalle.precio_venta}" for detalle in venta.detalles_venta])
    c.drawString(50, y, f"ID Venta: {venta.id_venta} - Fecha: {fecha} - Usuario: {venta.usuario.id_usuario} - Detalles: {detalles}")
    c.save()

    current_app.logger.debug(f"PDF generado exitosamente: {filename}")
