"""
CONTEXTO: PEDIDOS  -  capa de DOMINIO
-------------------------------------
AGREGADO Pedido: el Pedido es la RAIZ y las LineasDePedido solo se
crean o modifican a traves de el. Asi el total siempre es correcto.
"""
from dataclasses import dataclass, field
from enum import Enum

from catalogo.dominio import Dinero, ErrorDeDominio, Producto


class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"     # creado, esperando pago
    PAGADO = "pagado"           # pago aprobado (webhook en produccion)
    ENVIADO = "enviado"
    ENTREGADO = "entregado"


@dataclass(frozen=True)
class LineaDePedido:
    """Objeto de valor: copia el precio del momento de la compra."""
    producto_id: int
    nombre: str
    precio_unitario: Dinero
    cantidad: int

    @property
    def subtotal(self) -> Dinero:
        return self.precio_unitario.por(self.cantidad)


@dataclass
class Pedido:
    id: int | None
    comprador: str
    telefono: str
    metodo_pago: str
    lineas: list[LineaDePedido] = field(default_factory=list)
    estado: EstadoPedido = EstadoPedido.PENDIENTE
    codigo_pago: str = ""

    def agregar(self, producto: Producto, cantidad: int) -> None:
        if cantidad <= 0:
            raise ErrorDeDominio("La cantidad debe ser mayor a 0.")
        if not producto.hay_stock(cantidad):
            raise ErrorDeDominio(
                f"No hay stock suficiente de {producto.nombre}.")
        self.lineas.append(LineaDePedido(
            producto.id, producto.nombre, producto.precio, cantidad))

    @property
    def total(self) -> Dinero:
        total = Dinero(0)
        for linea in self.lineas:
            total = total + linea.subtotal
        return total

    def marcar_pagado(self, codigo: str) -> None:
        if not self.lineas:
            raise ErrorDeDominio("El pedido esta vacio.")
        self.estado = EstadoPedido.PAGADO
        self.codigo_pago = codigo
