"""PATRON REPOSITORIO para el agregado Pedido (se guarda completo)."""
from .dominio import Pedido
from .models import LineaPedidoModelo, PedidoModelo


class PedidoRepositorioDjango:
    def guardar(self, pedido: Pedido) -> Pedido:
        m = PedidoModelo.objects.create(
            comprador=pedido.comprador, telefono=pedido.telefono,
            metodo_pago=pedido.metodo_pago, estado=pedido.estado.value,
            codigo_pago=pedido.codigo_pago, total=pedido.total.monto)
        for linea in pedido.lineas:
            LineaPedidoModelo.objects.create(
                pedido=m, producto_id=linea.producto_id, nombre=linea.nombre,
                precio_unitario=linea.precio_unitario.monto,
                cantidad=linea.cantidad)
        pedido.id = m.id
        return pedido
