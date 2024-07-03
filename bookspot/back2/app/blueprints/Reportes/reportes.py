import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from modelos.modelo_movimiento import Movimiento  # Ajusta las importaciones según tu proyecto
from modelos.modelo_venta import Venta

def fetch_data():
    movimientos = Movimiento.query.all()
    ventas = Venta.query.all()
    return movimientos, ventas

def generate_pdf(movimientos, ventas):
    current_dir = os.path.dirname(__file__)  # Obtiene el directorio actual donde está este script
    report_path = os.path.join(current_dir, "reporte_movimientos_y_ventas.pdf")  # Construye la ruta completa
    
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter

    c.drawString(30, height - 30, f'Reporte generado el: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    y = height - 50
    c.drawString(30, y, 'Movimientos:')
    y -= 20
    for movimiento in movimientos:
        c.drawString(30, y, f'ID: {movimiento.id_movimiento}, Tipo: {movimiento.tipo_movimiento.nombre}, Fecha: {movimiento.fecha_hora}')
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 30
    
    y -= 20
    c.drawString(30, y, 'Ventas:')
    y -= 20
    for venta in ventas:
        c.drawString(30, y, f'ID: {venta.id_venta}, Usuario ID: {venta.id_usuario}, Monto: {venta.monto}, Fecha: {venta.fecha_venta}')
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 30

    c.save()

def main():
    movimientos, ventas = fetch_data()
    generate_pdf(movimientos, ventas)

if __name__ == '__main__':
    main()
