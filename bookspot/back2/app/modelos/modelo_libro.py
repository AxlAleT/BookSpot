from app import db

class Libro(db.Model):

    __tablename__ = 'libro'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, titulo, precio, available_quantity):
        self.titulo = titulo
        self.precio = precio
        self.available_quantity = available_quantity

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'precio': self.precio,
            'available_quantity': self.available_quantity
        }