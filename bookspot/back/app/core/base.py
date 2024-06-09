from app import db
from app.compartido.modelos.modelo_libro import Libro
from app.compartido.modelos.modelo_movimiento import Movimiento, TipoMovimiento, DetallesMovimiento
from .config import Config

config = Config()

def init_db():
    db.create_all()

def populate_books():

    books = [
        {"titulo": "El señor de los anillos", "precio": 15.99, "available_quantity": 10},
        {"titulo": "Cien años de soledad", "precio": 12.99, "available_quantity": 8},
        {"titulo": "Don Quijote de la Mancha", "precio": 14.99, "available_quantity": 5},
        {"titulo": "Matar a un ruiseñor", "precio": 9.99, "available_quantity": 12},
        {"titulo": "1984", "precio": 8.99, "available_quantity": 7},
        {"titulo": "Harry Potter y la piedra filosofal", "precio": 11.99, "available_quantity": 15},
        {"titulo": "Orgullo y prejuicio", "precio": 7.99, "available_quantity": 6},
        {"titulo": "El gran Gatsby", "precio": 10.99, "available_quantity": 9},
        {"titulo": "En busca del tiempo perdido", "precio": 13.99, "available_quantity": 4},
        {"titulo": "Ulises", "precio": 16.99, "available_quantity": 3},
    ]

    for book_data in books:
        book = Libro(**book_data)
        db.session.add(book)
    
    db.session.commit()
    print("Books have been added to the database.")


def init_tipos_movimiento():
    for tipo_data in config.TIPOS_MOVIMIENTO:
        tipo_existente = TipoMovimiento.query.filter_by(nombre=tipo_data['nombre']).first()
        if not tipo_existente:
            nuevo_tipo = TipoMovimiento(nombre=tipo_data['nombre'], descripcion=tipo_data['descripcion'])
            db.session.add(nuevo_tipo)
    db.session.commit()
