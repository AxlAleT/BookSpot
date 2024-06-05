from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from modelo_usuario import Usuario

class Apartado(Base):
    __tablename__ = 'apartado'
    id_apartado = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    fecha_limite = Column(DateTime)
    nombre_acreedor = Column(String)
    monto = Column(Float, nullable=False)
    usuario = relationship("Usuario", back_populates="apartados")
    detalles_apartado = relationship("DetalleApartado", back_populates="apartado")
