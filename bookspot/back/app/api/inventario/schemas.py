# Definir el esquema para la solicitud de agregar libro
from marshmallow import Schema, fields

class AddLibroSchema(Schema):
    titulo = fields.Str(required=True)
    precio = fields.Float(required=True)
    cantidad = fields.Int(required=True)