from marshmallow import Schema, fields

class LibroItemSchema(Schema):
    id_libro = fields.Int(required=True)
    cantidad = fields.Int(required=True)

class LibroResponseSchema(Schema):
    titulo = fields.Str(required=True)
    id_libro = fields.Int(required=True)
    precio = fields.Float(required=True)
    cantidad = fields.Int(required=True)

class VentaRequestSchema(Schema):
    items = fields.List(fields.Nested(LibroItemSchema), required=True)
    metodo_pago = fields.Str(required=True)

class VentaResponseSchema(Schema):
    books = fields.List(fields.Nested(LibroResponseSchema), required=True)