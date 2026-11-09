"""Rutas de la API de FeriaAndina (una seccion por contexto)."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from artesanos.api import ListaArtesanos
from catalogo.api import CategoriasAPI, ProductoDetalleAPI, ProductosAPI
from pedidos.api import PedidosAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    # Contexto Catalogo
    path("api/productos/", ProductosAPI.as_view()),
    path("api/productos/<int:pk>/", ProductoDetalleAPI.as_view()),
    path("api/categorias/", CategoriasAPI.as_view()),
    # Contexto Artesanos
    path("api/artesanos/", ListaArtesanos.as_view()),
    # Contexto Pedidos
    path("api/pedidos/", PedidosAPI.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
