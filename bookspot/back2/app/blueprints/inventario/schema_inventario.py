# Definir el esquema para la solicitud de agregar libro
from marshmallow import Schema, fields

class AddLibroSchema(Schema):
    titulo = fields.Str(required=True)
    precio = fields.Float(required=True)
    cantidad = fields.Int(required=True)

class EditLibroSchema(Schema):
    id = fields.Int(required=True)
    titulo = fields.Str(required=True)
    precio = fields.Float(required=True)
    available_quantity = fields.Int(required=True)

class SearchLibroSchema(Schema):
    keyword = fields.Str(required=True)