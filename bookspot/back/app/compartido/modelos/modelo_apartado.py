
from app import db
from .modelo_libro import Libro
from .modelo_usuario import Usuario

class Apartado(db.Model):
    __tablename__ = 'apartado'

    id_apartado = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_limite = db.Column(db.DateTime, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    nombre_acreedor = db.Column(db.String(100), nullable=False)

    usuario = db.relationship("Usuario", back_populates="apartados")
    detalles = db.relationship("DetallesApartado", back_populates="apartado")

    def __init__(self, id_usuario, fecha_limite, monto, nombre_acreedor):
        self.id_usuario = id_usuario
        self.fecha_limite = fecha_limite
        self.monto = monto
        self.nombre_acreedor = nombre_acreedor

    def to_dict(self):
        return {
            'id_apartado': self.id_apartado,
            'id_usuario': self.id_usuario,
            'fecha_limite': self.fecha_limite.isoformat() if self.fecha_limite else None,
            'monto': self.monto,
            'nombre_acreedor': self.nombre_acreedor,
            'detalles': [detalle.to_dict() for detalle in self.detalles]
        }

class DetallesApartado(db.Model):
    __tablename__ = 'detalles_apartado'

    id_detalle_apartado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_apartado = db.Column(db.Integer, db.ForeignKey('apartado.id_apartado'))
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_apartado = db.Column(db.Float, nullable=False)
    
    apartado = db.relationship("Apartado", back_populates="detalles")

    def __init__(self, id_apartado, id_libro, cantidad, precio_apartado):
        self.id_apartado = id_apartado
        self.id_libro = id_libro
        self.cantidad = cantidad
        self.precio_apartado = precio_apartado

    def to_dict(self):
        return {
            'id_detalle_apartado': self.id_detalle_apartado,
            'id_apartado': self.id_apartado,
            'id_libro': self.id_libro,
            'cantidad': self.cantidad,
            'precio_apartado': self.precio_apartado
        }

