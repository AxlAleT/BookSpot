from marshmallow import Schema, fields, validate, includes

class MovimientoSchema(Schema):
    id_tipo_movimiento = fields.Int(required=True)
    fecha_hora = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))

class VentaSchema(Schema):
    id_libro = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))
    precio_venta = fields.Float(required=True)
    fecha_venta = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')

class EntradaDatosSchema(Schema):
    movimientos = fields.List(fields.Nested(MovimientoSchema), required=True)
    ventas = fields.List(fields.Nested(VentaSchema), required=True)

