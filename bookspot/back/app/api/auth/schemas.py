from marshmallow import Schema, fields

class InicioSesionSchema(Schema):
    correo_electronico = fields.Email(required=True)
    password = fields.Str(required=True)