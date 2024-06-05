from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from modelo_libro import Libro
from modelo_tipo_movimiento import TipoMovimiento
from modelo_usuario import Usuario

class Movimiento(Base):
    __tablename__ = 'movimiento'
    id_movimiento = Column(Integer, primary_key=True)
    id_libro = Column(Integer, ForeignKey('libros.id_libro'))
    id_tipo_movimiento = Column(Integer, ForeignKey('tipo_movimiento.id_tipo_movimiento'))
    fecha_hora = Column(DateTime)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    cantidad = Column(Integer, nullable=False)
    libro = relationship("Libro", back_populates="movimientos")
    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    usuario = relationship("Usuario", back_populates="movimientos")
