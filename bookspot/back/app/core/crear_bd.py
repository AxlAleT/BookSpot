from compartido.modelos.modelo_metodo_pago import MetodoPago
from compartido.modelos.modelo_grupo import Grupo
from compartido.modelos.modelo_usuario import Usuario
from compartido.modelos.modelo_venta import Venta
from compartido.modelos.modelo_detalle_venta import DetalleVenta
from compartido.modelos.modelo_libro import Libro
from compartido.modelos.modelo_apartado import Apartado
from compartido.modelos.modelo_detalle_apartado import DetalleApartado
from compartido.modelos.modelo_tipo_movimiento import TipoMovimiento
from compartido.modelos.modelo_movimiento import Movimiento
from sqlalchemy.engine import reflection
from .base import engine, Base

# Funciones
def crear_tablas():
    """Crea las tablas en la base de datos si no existen."""
    inspector = reflection.Inspector.from_engine(engine)
    existing_tables = inspector.get_table_names()

    if not existing_tables or not all(
        table.__tablename__ in existing_tables for table in Base.metadata.tables.values()
    ):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Tablas creadas exitosamente.")
    else:
        print("Las tablas ya existen en la base de datos.")