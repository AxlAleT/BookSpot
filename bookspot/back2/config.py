
class AppConfig:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if AppConfig._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
            self.SQLALCHEMY_TRACK_MODIFICATIONS = False
            self.SECRET_KEY = 'your_secret_key'

            self.SESSION_TYPE = 'sqlalchemy'
            #from app import db
            #self.SESSION_SQLALCHEMY = db
            self.SESSION_SQLALCHEMY_TABLE = 'sesion'
            self.SESSION_PERMANENT = False

            AppConfig._instance = self

app_config = AppConfig()


class BDConfig:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if BDConfig._instance is not None:
            raise Exception("This class is a singleton!")
        else:

            self.TIPOS_MOVIMIENTO = [
                {'nombre': 'VPV', 'descripcion': 'Venta en Punto de Venta, relacionado a la venta de un producto en la tienda fisica'},
                {'nombre': 'APV', 'descripcion': 'Apartado en Punto de Venta, relacionado a un apartado de productos en el punto de venta'},
                {'nombre': 'RLI', 'descripcion': 'Registro de libro en inventario, registra la entrada de un libro en el inentario'},
                {'nombre': 'ELA', 'descripcion': 'Eliminacion de un apartado, cancelacion'},
                {'nombre': 'ACV', 'descripcion': 'Apartado Concretado, ahora es una Venta'},
            ]
            self.METODOS_PAGO = [
                {'nombre': 'TDC', 'descripcion': 'Pago con tarjeta de credito'},
                {'nombre': 'TDB', 'descripcion': 'Pago con tarjeta de debito'},
                {'nombre': 'EFE', 'descripcion': 'Pago con efectivo'},
            ]

            self.GRUPOS = [
                {'nombre': 'admin', 'descripcion': 'Grupo de administradores, con todos los permisos'},
                {'nombre': 'vendedor', 'descripcion': 'Grupo de vendedores, con permisos limitados'},
                {'nombre': 'almacenista', 'descripcion': 'Grupo de almacenistas, tienen permisos para hacer operaciones en el inventario'},
            ]

            self.USUARIOS = [
                {
                    'nombre': 'Usuario Admin',
                    'telefono': '555-0100',
                    'direccion': 'Calle Admin, 123',
                    'correo_electronico': 'admin@ejemplo.com',
                    'grupo': 'admin',
                    'password': 'password_seguro_admin'
                },
                {
                    'nombre': 'Usuario Vendedor',
                    'telefono': '555-0200',
                    'direccion': 'Calle Vendedor, 456',
                    'correo_electronico': 'vendedor@ejemplo.com',
                    'grupo': 'vendedor',
                    'password': 'password_seguro_vendedor'
                },
                {
                    'nombre': 'Usuario Almacenista',
                    'telefono': '555-0300',
                    'direccion': 'Calle Almacenista, 789',
                    'correo_electronico': 'almacenista@ejemplo.com',
                    'grupo': 'almacenista',
                    'password': 'password_seguro_almacenista'
                }
            ]

            BDConfig._instance = self

bdConfig = BDConfig()

class negocioConfig:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if negocioConfig._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.APARTADO_PORCENTAJE = 0.3
            negocioConfig._instance = self

negocio_config = negocioConfig()