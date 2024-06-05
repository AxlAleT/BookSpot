from core.base import Base
from core.base import engine
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


def crearBD():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)