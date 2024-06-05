from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from compartido.modelos.modelo_apartado import Apartado
from compartido.modelos.modelo_libro import Libro

class DetalleApartado(Base):
    __tablename__ = 'detalle_apartado'
    id_detalle_apartado = Column(Integer, primary_key=True)
    id_apartado = Column(Integer, ForeignKey('apartado.id_apartado'))
    id_libro = Column(Integer, ForeignKey('libros.id_libro'))
    cantidad = Column(Integer, nullable=False)
    precio_apartado = Column(Float, nullable=False)
    apartado = relationship("Apartado", back_populates="detalles_apartado")
    libro = relationship("Libro", back_populates="detalles_apartado")
