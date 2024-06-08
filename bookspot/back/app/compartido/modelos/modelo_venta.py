from app import db
from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha_venta = db.Column(db.DateTime, nullable=False, default=datetime.isoformat)

    def __init__(self, id_libro, cantidad, precio, monto, fecha_venta):
        self.id_libro = id_libro
        self.cantidad = cantidad
        self.precio = precio
        self.monto = monto
        self.fecha_venta = fecha_venta

    def to_dict(self):
        return {
            'id': self.id,
            'id_libro': self.id_libro,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'monto': self.monto,
            'fecha_venta': self.fecha_venta.isoformat()
        }