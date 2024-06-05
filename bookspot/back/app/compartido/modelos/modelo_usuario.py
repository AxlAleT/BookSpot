from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from compartido.modelos.modelo_grupo import Grupo

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    direccion = Column(String)
    correo_electronico = Column(String)
    id_rol = Column(Integer, ForeignKey('grupo.id_grupo'))
    grupo = relationship("Grupo", back_populates="usuarios")
