class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    TIPOS_MOVIMIENTO = [
        {'nombre': 'VPV', 'descripcion': 'Venta en Punto de Venta, relacionado a la venta de un producto en la tienda fisica'},
        {'nombre': 'APV', 'descripcion': 'Apartado en Punto de Venta, relacionado a un apartado de productos en el punto de venta'},
        {'nombre': 'RLI', 'descripcion': 'Registro de libro en inventario, registra la entrada de un libro en el inentario'},
    ]
    METODOS_PAGO = [
        {'nombre': 'TDC', 'descripcion': 'Pago con tarjeta de credito'},
        {'nombre': 'TDB', 'descripcion': 'Pago con tarjeta de debito'},
        {'nombre': 'EFE', 'descripcion': 'Pago con efectivo'},
    ]

