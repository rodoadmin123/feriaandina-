"""
CONTEXTO: CATALOGO  -  capa de INFRAESTRUCTURA (persistencia)
--------------------------------------------------------------
El modelo de Django solo sabe GUARDAR datos en la base de datos.
Las reglas del negocio estan en dominio.py.
"""
from django.db import models

from artesanos.models import Artesano

from .dominio import Categoria


class ProductoModelo(models.Model):
    CATEGORIAS = [(c.value, c.name.capitalize()) for c in Categoria]

    artesano = models.ForeignKey(
        Artesano, on_delete=models.PROTECT, related_name="productos")
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    foto = models.ImageField(upload_to="productos/", blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "producto"

    def __str__(self):
        return self.nombre
