"""
Capa de PRESENTACION (API REST). Las vistas son delgadas: reciben la
peticion HTTP, llaman al servicio y devuelven JSON.
"""
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .dominio import Categoria, ErrorDeDominio
from .models import ProductoModelo
from .repositorios import ProductoRepositorioDjango
from .serializers import ProductoSalida
from .servicios import ConsultarCatalogo, PublicarProducto


class ProductosAPI(APIView):
    # MultiPart: permite recibir la foto tomada con el celular
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        """GET /api/productos/?categoria=textiles&q=manta"""
        productos = ConsultarCatalogo().ejecutar(
            categoria=request.query_params.get("categoria"),
            texto=request.query_params.get("q"),
        )
        datos = ProductoSalida(productos, many=True,
                               context={"request": request}).data
        return Response(datos)

    def post(self, request):
        """POST /api/productos/  (formulario 'Vender' del artesano)"""
        campos = ["artesano_id", "nombre", "precio", "stock",
                  "categoria", "descripcion"]
        datos = {c: request.data.get(c) for c in campos}
        try:
            producto = PublicarProducto().ejecutar(
                datos, foto=request.FILES.get("foto"))
        except ErrorDeDominio as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductoSalida(producto,
                                       context={"request": request}).data,
                        status=status.HTTP_201_CREATED)


class ProductoDetalleAPI(APIView):
    def get(self, request, pk):
        """GET /api/productos/5/"""
        try:
            producto = ProductoRepositorioDjango().obtener(pk)
        except ProductoModelo.DoesNotExist:
            return Response({"error": "Producto no encontrado"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(ProductoSalida(producto,
                                       context={"request": request}).data)


class CategoriasAPI(APIView):
    def get(self, request):
        """GET /api/categorias/  -> lista cerrada del dominio"""
        nombres = {"textiles": "Textiles", "ceramica": "Cerámica",
                   "mates": "Mates burilados", "cafe": "Café",
                   "granos": "Granos andinos"}
        return Response([{"id": c.value, "nombre": nombres[c.value]}
                         for c in Categoria])
