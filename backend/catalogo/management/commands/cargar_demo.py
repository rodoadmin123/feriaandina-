"""
python manage.py cargar_demo
Carga artesanos y productos FICTICIOS para probar el prototipo.
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from artesanos.models import Artesano
from catalogo.models import ProductoModelo
from pedidos.models import PedidoModelo

FOTOS = Path(__file__).resolve().parents[2] / "demo_fotos"

ARTESANOS = [
    ("Rosa Huamán", "Hualhuas", "Tejedora", "964000111"),
    ("Elena Poma", "Cochas Chico", "Mates burilados", "964000222"),
    ("Julián Rojas", "Aco", "Ceramista", "964000333"),
    ("Marco Quispe", "Pangoa", "Caficultor", "964000444"),
    ("Lucia Canchari", "Jauja", "Agricultora", "964000555"),
]

# (artesano, nombre, categoria, precio, stock, foto, descripcion)
PRODUCTOS = [
    (0, "Manta tejida de Hualhuas", "textiles", "180.00", 6, "manta.jpg",
     "Manta de lana de oveja teñida con tintes naturales. 1.20 x 1.60 m."),
    (0, "Tapiz rombo andino", "textiles", "140.00", 3, "tapiz.jpg",
     "Tapiz para pared tejido en telar de pedal."),
    (0, "Chalina de alpaca", "textiles", "65.00", 12, "chalina.jpg",
     "Chalina suave de fibra de alpaca, colores tierra."),
    (1, "Mate burilado festivo", "mates", "95.00", 4, "mate.jpg",
     "Calabaza burilada a mano con escenas de la fiesta patronal."),
    (2, "Cántaro de cerámica de Aco", "ceramica", "70.00", 5, "cantaro.jpg",
     "Cántaro de arcilla cocida con decoración blanca tradicional."),
    (3, "Café de altura tostado 500 g", "cafe", "38.00", 30, "cafe.jpg",
     "Café arábica de Pangoa, tostado medio, en grano."),
    (4, "Quinua blanca 1 kg", "granos", "18.00", 40, "quinua.jpg",
     "Quinua lavada, cosecha de la campaña actual."),
]


class Command(BaseCommand):
    help = "Carga datos de prueba de FeriaAndina"

    def handle(self, *args, **opciones):
        PedidoModelo.objects.all().delete()
        ProductoModelo.objects.all().delete()
        Artesano.objects.all().delete()
        artesanos = [Artesano.objects.create(nombre=n, comunidad=c, oficio=o,
                                             telefono=t)
                     for n, c, o, t in ARTESANOS]
        for a, nombre, cat, precio, stock, foto, desc in PRODUCTOS:
            p = ProductoModelo(artesano=artesanos[a], nombre=nombre,
                               categoria=cat, precio=precio, stock=stock,
                               descripcion=desc)
            with open(FOTOS / foto, "rb") as f:
                p.foto.save(foto, File(f), save=True)
        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(artesanos)} artesanos y {len(PRODUCTOS)} productos."))
