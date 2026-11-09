"""
CONTEXTO: PEDIDOS - SERVICIO DE APLICACION "RealizarPedido"
Une los pasos 5, 6 y 7 del proceso del IDL1:
  carrito -> verificar stock -> pagar -> descontar stock -> guardar.
transaction.atomic(): si algo falla, la base de datos vuelve atras
(no queda un pedido pagado sin descontar stock, ni al reves).
"""
from django.db import transaction

from catalogo.dominio import ErrorDeDominio
from catalogo.models import ProductoModelo
from catalogo.repositorios import ProductoRepositorioDjango

from .dominio import Pedido
from .pagos import obtener_metodo
from .repositorios import PedidoRepositorioDjango


class RealizarPedido:
    def __init__(self):
        self.productos = ProductoRepositorioDjango()
        self.pedidos = PedidoRepositorioDjango()

    @transaction.atomic
    def ejecutar(self, comprador, telefono, metodo_pago, items) -> Pedido:
        if not comprador or not telefono:
            raise ErrorDeDominio("Escribe tu nombre y tu celular.")
        if not items:
            raise ErrorDeDominio("El carrito esta vacio.")

        pedido = Pedido(None, comprador, telefono, metodo_pago)
        productos = []
        for item in items:
            try:
                producto = self.productos.obtener(int(item["producto_id"]))
            except ProductoModelo.DoesNotExist:
                raise ErrorDeDominio("Un producto del carrito ya no existe.")
            cantidad = int(item["cantidad"])
            pedido.agregar(producto, cantidad)     # regla: hay stock
            productos.append((producto, cantidad))

        # Patron Estrategia: el metodo de pago se elige en tiempo real
        codigo = obtener_metodo(metodo_pago).cobrar(pedido.total, "FA")
        pedido.marcar_pagado(codigo)

        # Recien con el pago aprobado se descuenta el stock (IDL1)
        for producto, cantidad in productos:
            producto.descontar_stock(cantidad)
            self.productos.guardar(producto)

        return self.pedidos.guardar(pedido)
