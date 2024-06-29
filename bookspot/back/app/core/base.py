from app import db
from app.compartido.modelos.modelo_libro import Libro
from app.compartido.modelos.modelo_movimiento import Movimiento, TipoMovimiento, DetallesMovimiento
from .config import Config
from app.compartido.modelos.modelo_metodo_pago import MetodoPago
from app.compartido.modelos.modelo_grupo import Grupo
from app.compartido.modelos.modelo_usuario import Usuario


config = Config()

def init_db():
    db.drop_all()
    db.create_all()
    populate_books()
    init_tipos_movimiento()
    init_metodos_pago()
    init_grupos()
    init_usuarios()

def populate_books():

    books = [
        {"titulo": "El señor de los anillos", "precio": 15.99, "available_quantity": 300},
        {"titulo": "Cien años de soledad", "precio": 12.99, "available_quantity": 800},
        {"titulo": "Don Quijote de la Mancha", "precio": 14.99, "available_quantity": 500},
        {"titulo": "Matar a un ruiseñor", "precio": 9.99, "available_quantity": 1200},
        {"titulo": "1984", "precio": 8.99, "available_quantity": 700},
        {"titulo": "Harry Potter y la piedra filosofal", "precio": 11.99, "available_quantity": 1500},
        {"titulo": "Orgullo y prejuicio", "precio": 7.99, "available_quantity": 600},
        {"titulo": "El gran Gatsby", "precio": 10.99, "available_quantity": 900},
        {"titulo": "En busca del tiempo perdido", "precio": 13.99, "available_quantity": 400},
        {"titulo": "Ulises", "precio": 16.99, "available_quantity": 300},
    ]

    for book_data in books:
        book = Libro(**book_data)
        db.session.add(book)
    
    db.session.commit()
    print("Books have been added to the database.")


def init_tipos_movimiento():
    """Inserta tipos de movimiento en la base de datos sin verificar si ya existen."""
    for tipo_data in config.TIPOS_MOVIMIENTO:
        nuevo_tipo = TipoMovimiento(nombre=tipo_data['nombre'], descripcion=tipo_data['descripcion'])
        db.session.add(nuevo_tipo)
    db.session.commit()

def init_metodos_pago():
    """Inserta métodos de pago en la base de datos sin verificar si ya existen."""
    for metodo_data in config.METODOS_PAGO:
        nuevo_metodo = MetodoPago(nombre=metodo_data['nombre'], descripcion=metodo_data['descripcion'])
        db.session.add(nuevo_metodo)
    db.session.commit()

def init_grupos():
    """Inserta grupos en la base de datos sin verificar si ya existen."""
    for grupo_data in config.GRUPOS:
        nuevo_grupo = Grupo(nombre=grupo_data['nombre'], descripcion=grupo_data['descripcion'])
        db.session.add(nuevo_grupo)
    db.session.commit()

def init_usuarios():
    """Inserta usuarios por defecto en la base de datos sin verificar si ya existen."""
    for usuario_data in config.USUARIOS_POR_DEFECTO:
        # Buscar el grupo por nombre para obtener su ID
        grupo = Grupo.query.filter_by(nombre=usuario_data['grupo']).first()
        if grupo:
            nuevo_usuario = Usuario(
                nombre=usuario_data['nombre'],
                telefono=usuario_data['telefono'],
                direccion=usuario_data['direccion'],
                correo_electronico=usuario_data['correo_electronico'],
                id_grupo=grupo.id,
                password=usuario_data['password']
            )
            db.session.add(nuevo_usuario)
    db.session.commit()