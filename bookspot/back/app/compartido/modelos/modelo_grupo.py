from sqlalchemy import Column, Integer, String
from core.base import Base

class Grupo(Base):
    __tablename__ = 'grupo'
    id_grupo = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    permisos = Column(String)
