"""Rutas de la API de FeriaAndina (una seccion por contexto)."""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from artesanos.api import ListaArtesanos
from catalogo.api import CategoriasAPI, ProductoDetalleAPI, ProductosAPI
from pedidos.api import PedidosAPI

from .spa import pagina_react

admin.site.site_header = "FeriaAndina · Administración"
admin.site.site_title = "FeriaAndina"
admin.site.index_title = "Panel del equipo"

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
]

# Fotos guardadas en disco (tu PC, o el servidor si aun no hay Cloudinary)
if not settings.USA_CLOUDINARY:
    urlpatterns.append(
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}))

# Cualquier otra ruta la resuelve React (solo existe si se compilo el front-end)
urlpatterns.append(re_path(r"^(?!api/|admin/|media/|static/)(?P<ruta>.*)$", pagina_react))
