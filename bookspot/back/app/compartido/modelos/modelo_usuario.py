from app import db
from .modelo_grupo import Grupo
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    password_hash = db.Column(db.String(128))  # Campo para el hash de la contraseña

    grupo = db.relationship("Grupo", back_populates="usuarios")
    ventas = db.relationship("Venta", back_populates="usuario")
    apartados = db.relationship("Apartado", back_populates="usuario")

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
            'correo_electronico': self.correo_electronico,
            'id_grupo': self.id_grupo
        }