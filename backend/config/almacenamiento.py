"""
ADAPTADOR de almacenamiento de fotos hacia Cloudinary (tecnologia elegida en el IDL1).

Django guarda archivos a traves de una clase "Storage". Esta implementacion sube
las fotos a Cloudinary en lugar del disco local. El resto del sistema (modelos,
repositorios, servicios) no cambia: es el mismo principio del patron Repositorio.

Se activa solo si existe la variable de entorno CLOUDINARY_URL
(formato: cloudinary://API_KEY:API_SECRET@CLOUD_NAME).
"""
from pathlib import PurePosixPath

import cloudinary
import cloudinary.uploader
import cloudinary.utils
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

CARPETA = "feriaandina"


@deconstructible
class AlmacenamientoCloudinary(Storage):

    @staticmethod
    def _separar(nombre: str):
        ruta = PurePosixPath(nombre)
        return str(ruta.with_suffix("")), ruta.suffix.lstrip(".") or "jpg"

    def _save(self, name, content):
        public_id, _ = self._separar(f"{CARPETA}/{name}")
        if hasattr(content, "seek"):
            content.seek(0)
        resultado = cloudinary.uploader.upload(
            content, public_id=public_id, unique_filename=True, overwrite=False,
            resource_type="image")
        # Se guarda en la base de datos como "carpeta/archivo.formato"
        return f"{resultado['public_id']}.{resultado['format']}"

    def url(self, name):
        public_id, formato = self._separar(name)
        url, _ = cloudinary.utils.cloudinary_url(
            public_id, format=formato, secure=True,
            width=900, crop="limit", quality="auto")
        return url

    def exists(self, name):
        return False  # Cloudinary evita nombres repetidos con unique_filename

    def get_available_name(self, name, max_length=None):
        return name

    def delete(self, name):
        public_id, _ = self._separar(name)
        cloudinary.uploader.destroy(public_id, resource_type="image")

    def size(self, name):
        return 0
