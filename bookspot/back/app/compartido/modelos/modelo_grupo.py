from app import db

class Grupo(db.Model):
    __tablename__ = 'grupo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    permisos = db.Column(db.String(255), nullable=True)

    usuarios = db.relationship("Usuario", back_populates="grupo")

    def __init__(self, nombre, descripcion, permisos):
        self.nombre = nombre
        self.descripcion = descripcion
        self.permisos = permisos

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'permisos': self.permisos
        }
}

