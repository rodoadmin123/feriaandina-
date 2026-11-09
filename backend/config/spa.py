"""Entrega la pagina de React compilada para cualquier ruta del front-end (/, /vender, /carrito...)."""
from django.conf import settings
from django.http import FileResponse, Http404


def pagina_react(request, ruta=""):
    indice = settings.FRONTEND_DIST / "index.html"
    if not indice.exists():
        raise Http404("El front-end no esta compilado. En desarrollo abre http://localhost:5173")
    return FileResponse(open(indice, "rb"), content_type="text/html")
