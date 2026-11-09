from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from catalogo.dominio import ErrorDeDominio

from .servicios import RealizarPedido


class PedidosAPI(APIView):
    def post(self, request):
        """POST /api/pedidos/
        {"comprador": "...", "telefono": "...", "metodo_pago": "yape",
         "items": [{"producto_id": 1, "cantidad": 2}]}"""
        d = request.data
        try:
            pedido = RealizarPedido().ejecutar(
                d.get("comprador"), d.get("telefono"),
                d.get("metodo_pago"), d.get("items", []))
        except ErrorDeDominio as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "id": pedido.id,
            "estado": pedido.estado.value,
            "codigo_pago": pedido.codigo_pago,
            "total": str(pedido.total.monto),
            "lineas": [{"nombre": l.nombre, "cantidad": l.cantidad,
                        "subtotal": str(l.subtotal.monto)}
                       for l in pedido.lineas],
        }, status=status.HTTP_201_CREATED)
