"""
python manage.py crear_admin
Crea el usuario administrador a partir de las variables de entorno
DJANGO_ADMIN_USUARIO y DJANGO_ADMIN_CLAVE (y opcional DJANGO_ADMIN_CORREO).
Si ya existe, no hace nada. Pensado para Render gratis, que no tiene consola.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el administrador desde variables de entorno (si no existe)."

    def handle(self, *args, **opciones):
        usuario = os.environ.get("DJANGO_ADMIN_USUARIO")
        clave = os.environ.get("DJANGO_ADMIN_CLAVE")
        if not usuario or not clave:
            self.stdout.write("Sin DJANGO_ADMIN_USUARIO / DJANGO_ADMIN_CLAVE: no se crea administrador.")
            return
        Usuario = get_user_model()
        if Usuario.objects.filter(username=usuario).exists():
            self.stdout.write(f"El administrador «{usuario}» ya existe.")
            return
        Usuario.objects.create_superuser(usuario, os.environ.get("DJANGO_ADMIN_CORREO", ""), clave)
        self.stdout.write(self.style.SUCCESS(f"Administrador «{usuario}» creado."))
