"""
CONTEXTO: ARTESANOS
-------------------
Guarda quien vende en FeriaAndina. Es un contexto sencillo (solo
registrar y consultar), por eso usamos directamente el modelo de
Django: en DDD no todo contexto necesita todas las capas.
"""
from django.db import models


class Artesano(models.Model):
    # Lenguaje ubicuo: usamos las mismas palabras que usa Andrea
    nombre = models.CharField(max_length=120)
    comunidad = models.CharField(max_length=80)      # ej. Hualhuas
    oficio = models.CharField(max_length=80)         # ej. Tejedora
    telefono = models.CharField(max_length=15)       # para avisos por WhatsApp

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.comunidad})"
