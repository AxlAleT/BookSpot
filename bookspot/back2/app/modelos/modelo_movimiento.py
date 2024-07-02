from app import db
from .modelo_libro import Libro

class Movimiento(db.Model):
    __tablename__ = 'movimiento'

    id_movimiento = db.Column(db.Integer, primary_key=True)
    id_tipo_movimiento = db.Column(db.Integer, db.ForeignKey('tipo_movimiento.id_tipo_movimiento'))
    fecha_hora = db.Column(db.DateTime)

    tipo_movimiento = db.relationship("TipoMovimiento", back_populates="movimientos")
    detalles = db.relationship("DetallesMovimiento", back_populates="movimiento")

    def __init__(self, id_tipo_movimiento, fecha_hora):
        self.id_tipo_movimiento = id_tipo_movimiento
        self.fecha_hora = fecha_hora

    def to_dict(self):
        return {
            'id_movimiento': self.id_movimiento,
            'id_tipo_movimiento': self.id_tipo_movimiento,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None
        }

class DetallesMovimiento(db.Model):
    __tablename__ = 'detalles_movimiento'

    id_detalle_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_movimiento = db.Column(db.Integer, db.ForeignKey('movimiento.id_movimiento'))
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    
    movimiento = db.relationship("Movimiento", back_populates="detalles")

    def __init__(self, id_movimiento, id_libro, cantidad):
        self.id_movimiento = id_movimiento
        self.id_libro = id_libro
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'id_detalle_movimiento': self.id_detalle_movimiento,
            'id_movimiento': self.id_movimiento,
            'id_libro': self.id_libro,
            'cantidad': self.cantidad
        }

class TipoMovimiento(db.Model):
    __tablename__ = 'tipo_movimiento'

    id_tipo_movimiento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String)
    movimientos = db.relationship("Movimiento", back_populates="tipo_movimiento")

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self):
        return {
            'id_tipo_movimiento': self.id_tipo_movimiento,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }