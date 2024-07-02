from app import db  

class MetodoPago(db.Model):
    __tablename__ = 'metodo_pago'

    id_metodo_pago = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # Adjusted length for flexibility
    descripcion = db.Column(db.Text)  # Use Text for potentially longer descriptions

    # Constructor for convenient object creation
    def __init__(self, nombre, descripcion=None):  
        self.nombre = nombre
        self.descripcion = descripcion

    # Method to convert the object to a dictionary for easy serialization
    def to_dict(self):
        return {
            'id_metodo_pago': self.id_metodo_pago,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }