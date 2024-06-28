from app import db
from .modelo_libro import Libro
from .modelo_usuario import Usuario

class Venta(db.Model):
    __tablename__ = 'venta'

    id_venta = db.Column(db.Integer, primary_key=True)
    fecha_venta = db.Column(db.DateTime, nullable=False)
    #id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)

    #usuario = db.relationship("Usuario", back_populates="ventas")
    detalles = db.relationship("DetallesVenta", back_populates="venta")

    def __init__(self, fecha_venta, monto):
        self.fecha_venta = fecha_venta
        #self.id_usuario = id_usuario
        self.monto = monto

    def to_dict(self):
        return {
            'id_venta': self.id_venta,
            'fecha_venta': self.fecha_venta.isoformat() if self.fecha_venta else None,
            #'id_usuario': self.id_usuario,
            'monto': self.monto,
            'detalles': [detalle.to_dict() for detalle in self.detalles]
        }

class DetallesVenta(db.Model):
    __tablename__ = 'detalles_venta'

    id_detalle_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'))
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    
    venta = db.relationship("Venta", back_populates="detalles")

    def __init__(self, id_venta, id_libro, cantidad, precio_venta):
        self.id_venta = id_venta
        self.id_libro = id_libro
        self.cantidad = cantidad
        self.precio_venta = precio_venta

    def to_dict(self):
        return {
            'id_detalle_venta': self.id_detalle_venta,
            'id_venta': self.id_venta,
            'id_libro': self.id_libro,
            'cantidad': self.cantidad,
            'precio_venta': self.precio_venta
        }