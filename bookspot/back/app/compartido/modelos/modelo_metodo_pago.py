from sqlalchemy import Column, Integer, String
from core.base import Base

class MetodoPago(Base):
    __tablename__ = 'metodo_pago'
    id_metodo_pago = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
