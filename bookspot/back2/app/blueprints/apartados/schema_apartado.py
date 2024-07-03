from marshmallow import Schema, fields

class LibroItemSchema(Schema):
    id_libro = fields.Int(required=True)
    cantidad = fields.Int(required=True)
    precio_apartado = fields.Float(required=True)

class ApartadoRequestSchema(Schema):
    monto = fields.Float(required=True)
    nombre_acreedor = fields.Str(required=True)
    items = fields.List(fields.Nested(LibroItemSchema), required=True)

class ApartadoResponseSchema(Schema):
    id_apartado = fields.Int(required=True)
    id_usuario = fields.Int(required=True)
    fecha_limite = fields.DateTime(required=True)
    monto = fields.Float(required=True)
    nombre_acreedor = fields.Str(required=True)
    detalles = fields.List(fields.Nested(LibroItemSchema), required=True)