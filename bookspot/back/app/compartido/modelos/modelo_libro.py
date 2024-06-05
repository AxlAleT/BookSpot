from core.base import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Libro(Base):
    __tablename__ = 'libros'
    id_libro = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    autor = Column(String)
    editorial = Column(String)
    cantidad = Column(Integer)
    precio = Column(Float)
    detalles_venta = relationship("DetalleVenta", back_populates="libro")
    detalles_apartado = relationship("DetalleApartado", back_populates="libro")
    movimientos = relationship("Movimiento", back_populates="libro")

