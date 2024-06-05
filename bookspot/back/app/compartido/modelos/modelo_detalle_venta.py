from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from compartido.modelos.modelo_venta import Venta
from compartido.modelos.modelo_libro import Libro

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id_detalle_venta = Column(Integer, primary_key=True)
    id_venta = Column(Integer, ForeignKey('venta.id_venta'))
    cantidad = Column(Integer, nullable=False)
    precio_venta = Column(Float, nullable=False)
    id_libro = Column(Integer, ForeignKey('libros.id_libro'))
    venta = relationship("Venta", back_populates="detalles_venta")
    libro = relationship("Libro", back_populates="detalles_venta")
