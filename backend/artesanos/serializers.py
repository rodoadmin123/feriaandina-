from rest_framework import serializers

from .models import Artesano


class ArtesanoSerializer(serializers.ModelSerializer):
    """Convierte un Artesano en JSON para el front-end."""

    class Meta:
        model = Artesano
        fields = ["id", "nombre", "comunidad", "oficio"]
