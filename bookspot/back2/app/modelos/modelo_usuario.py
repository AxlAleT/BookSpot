from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from .modelo_grupo import Grupo

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    ventas = db.relationship("Venta", back_populates="usuario")

    def __init__(self, nombre, telefono, direccion, correo_electronico, id_grupo, password):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo_electronico = correo_electronico
        self.id_grupo = id_grupo
        self.set_password(password)

    def set_password(self, password):
        """Genera el hash de la contraseña y lo guarda en el campo password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'id_grupo' : self.id_grupo,
            'correo_electronico': self.correo_electronico,
        }