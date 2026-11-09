from rest_framework import generics

from .models import Artesano
from .serializers import ArtesanoSerializer


class ListaArtesanos(generics.ListAPIView):
    """GET /api/artesanos/  -> lista de artesanos (para el selector "Vendo como")."""
    queryset = Artesano.objects.all()
    serializer_class = ArtesanoSerializer
