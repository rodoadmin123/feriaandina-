"""CONTEXTO: PEDIDOS - persistencia con el ORM de Django."""
from django.db import models

from .dominio import EstadoPedido


class PedidoModelo(models.Model):
    ESTADOS = [(e.value, e.name.capitalize()) for e in EstadoPedido]

    comprador = models.CharField(max_length=120)
    telefono = models.CharField(max_length=15)
    metodo_pago = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    codigo_pago = models.CharField(max_length=40, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "pedido"

    def __str__(self):
        return f"Pedido {self.id} - {self.comprador}"


class LineaPedidoModelo(models.Model):
    pedido = models.ForeignKey(PedidoModelo, on_delete=models.CASCADE,
                               related_name="lineas")
    # Solo guardamos el ID: otro contexto (Catalogo) es dueno del Producto
    producto_id = models.IntegerField()
    nombre = models.CharField(max_length=120)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    cantidad = models.PositiveIntegerField()
