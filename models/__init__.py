# models/__init__.py
# Este archivo hace que la carpeta models sea un paquete Python

from .contacto import Contacto
from .database import BaseDatos

__all__ = ['Contacto', 'BaseDatos']