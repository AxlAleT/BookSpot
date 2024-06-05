from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from modelo_usuario import Usuario

class Venta(Base):
    __tablename__ = 'venta'
    id_venta = Column(Integer, primary_key=True)
    monto = Column(Float, nullable=False)
    fecha_venta = Column(DateTime)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    usuario = relationship("Usuario", back_populates="ventas")
