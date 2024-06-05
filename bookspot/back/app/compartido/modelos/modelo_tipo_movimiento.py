from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.base import Base

class TipoMovimiento(Base):
    __tablename__ = 'tipo_movimiento'
    id_tipo_movimiento = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    movimientos = relationship("Movimiento", back_populates="tipo_movimiento")
