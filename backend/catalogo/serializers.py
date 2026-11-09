from rest_framework import serializers

from artesanos.models import Artesano


class ProductoSalida(serializers.Serializer):
    """Arma el JSON que recibe React a partir de la entidad de dominio."""
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    descripcion = serializers.CharField()
    categoria = serializers.CharField(source="categoria.value")
    precio = serializers.DecimalField(
        source="precio.monto", max_digits=8, decimal_places=2)
    stock = serializers.IntegerField()
    foto_url = serializers.SerializerMethodField()
    artesano = serializers.SerializerMethodField()

    def get_foto_url(self, producto):
        request = self.context.get("request")
        if producto.foto_url and request:
            return request.build_absolute_uri(producto.foto_url)
        return producto.foto_url

    def get_artesano(self, producto):
        a = Artesano.objects.get(pk=producto.artesano_id)
        return {"id": a.id, "nombre": a.nombre, "comunidad": a.comunidad}
