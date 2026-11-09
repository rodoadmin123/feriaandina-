"""
Carga artesanos y productos FICTICIOS para probar y mostrar FeriaAndina.

  python manage.py cargar_demo             # carga solo si no hay productos (seguro en el servidor)
  python manage.py cargar_demo --reiniciar # BORRA artesanos, productos y pedidos y vuelve a cargar

Todos los nombres de personas son inventados; las comunidades son reales del
Valle del Mantaro y alrededores (Junín) para dar contexto.
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from artesanos.models import Artesano
from catalogo.models import ProductoModelo
from pedidos.models import PedidoModelo

FOTOS = Path(__file__).resolve().parents[2] / "demo_fotos"

# clave: (nombre, comunidad, oficio, telefono ficticio)
ARTESANOS = {
    "rosa": ("Rosa Huamán", "Hualhuas", "Tejedora", "900000101"),
    "teodoro": ("Teodoro Ccanto", "San Pedro de Cajas", "Tapicero", "900000102"),
    "benita": ("Benita Huaroc", "Viques", "Tejedora de fajas", "900000103"),
    "elena": ("Elena Poma", "Cochas Chico", "Mates burilados", "900000104"),
    "marisol": ("Marisol Yauri", "Cochas Grande", "Mates burilados", "900000105"),
    "julian": ("Julián Rojas", "Aco", "Ceramista", "900000106"),
    "felipe": ("Felipe Rivera", "Quilcas", "Ceramista", "900000107"),
    "marco": ("Marco Quispe", "Pangoa", "Caficultor", "900000108"),
    "hugo": ("Hugo Pariona", "Satipo", "Caficultor", "900000109"),
    "lucia": ("Lucía Canchari", "Jauja", "Agricultora", "900000110"),
}

# (artesano, nombre, categoria, precio, stock, foto, descripcion)
PRODUCTOS = [
    ("rosa", "Manta tejida de Hualhuas", "textiles", "180.00", 6, "manta",
     "Manta de lana de oveja teñida con tintes naturales de cochinilla y nogal. Tejida en telar de pedal. Mide 1.20 × 1.60 m."),
    ("marco", "Café de altura tostado 500 g", "cafe", "38.00", 30, "cafe",
     "Café arábica cultivado a 1 600 m s. n. m. en Pangoa. Tostado medio, en grano, con notas a chocolate y panela."),
    ("elena", "Mate burilado festivo", "mates", "95.00", 4, "mate",
     "Calabaza burilada a mano con buril de acero. Representa escenas de la fiesta patronal de Cochas."),
    ("julian", "Cántaro de cerámica de Aco", "ceramica", "70.00", 5, "cantaro",
     "Cántaro de arcilla cocida en horno de leña, con la decoración blanca tradicional de Aco. Capacidad de 2 litros."),
    ("lucia", "Quinua blanca 1 kg", "granos", "18.00", 40, "quinua",
     "Quinua lavada y seleccionada, lista para cocinar. Cosechada en las chacras de Jauja."),
    ("teodoro", "Tapiz rombo andino", "textiles", "140.00", 3, "tapiz",
     "Tapiz para pared con el rombo escalonado andino, en lana de oveja. Incluye listón de madera para colgar."),
    ("marisol", "Mate «Fiesta del Santiago»", "mates", "120.00", 3, "mate_santiago",
     "Mate burilado que narra la fiesta del Santiago: músicos, danzantes y la marcación del ganado."),
    ("felipe", "Juego de 2 tazas de Quilcas", "ceramica", "48.00", 10, "tazas",
     "Par de tazas de cerámica esmaltada, aptas para bebidas calientes. Pintadas a mano con franjas blancas."),
    ("hugo", "Café especial de Satipo 250 g", "cafe", "45.00", 15, "cafe_especial",
     "Microlote de café especial con puntaje de taza 85. Notas florales y a frutos rojos. Tostado claro."),
    ("rosa", "Chalina de alpaca", "textiles", "65.00", 12, "chalina",
     "Chalina suave de fibra de alpaca en colores tierra. Abriga sin picar; ideal para el frío de la sierra."),
    ("lucia", "Kiwicha 500 g", "granos", "12.00", 25, "kiwicha",
     "Kiwicha limpia, rica en proteínas. Se puede reventar como canchita o usar en mazamorras."),
    ("benita", "Faja tejida (chumpi) de Viques", "textiles", "55.00", 9, "faja",
     "Faja tradicional tejida en telar de cintura, con motivos de rombos. Mide 2.20 m de largo."),
    ("elena", "Azucarero de mate burilado", "mates", "70.00", 6, "mate_azucarero",
     "Azucarero hecho de calabaza burilada con tapa. Pieza útil y decorativa para la mesa."),
    ("julian", "Plato decorativo de Aco", "ceramica", "55.00", 7, "plato",
     "Plato de cerámica para colgar, con sol central y puntos azules pintados a mano. 30 cm de diámetro."),
    ("marco", "Café verde en grano 1 kg", "cafe", "50.00", 12, "cafe_verde",
     "Café verde sin tostar para quienes tuestan en casa. Variedad típica y caturra."),
    ("teodoro", "Tapiz «Paisaje del Mantaro»", "textiles", "320.00", 2, "tapiz_paisaje",
     "Tapiz grande que muestra el nevado Huaytapallana y las chacras del valle. Pieza única de 1.00 × 0.80 m."),
    ("marisol", "Mate lámpara burilada", "mates", "150.00", 3, "mate_lampara",
     "Lámpara colgante de calabaza perforada y burilada. Proyecta puntos de luz cálida. Incluye cable y foco LED."),
    ("lucia", "Maíz morado 1 kg", "granos", "9.00", 35, "maiz_morado",
     "Maíz morado seleccionado para chicha morada y mazamorra. Color intenso."),
    ("felipe", "Maceta pintada de Quilcas", "ceramica", "40.00", 14, "maceta",
     "Maceta de barro con franjas amarillas y azules. Tiene orificio de drenaje. 20 cm de alto."),
    ("benita", "Bolso tejido de Viques", "textiles", "75.00", 8, "bolso",
     "Bolso de mano tejido con asa de cuero, forrado por dentro. Diseños de rombos en colores vivos."),
    ("hugo", "Café molido 250 g", "cafe", "22.00", 28, "cafe_molido",
     "Café de Satipo molido para pasado o cafetera italiana. Tostado oscuro, sabor intenso."),
    ("rosa", "Chullo de lana de oveja", "textiles", "45.00", 10, "chullo",
     "Chullo tejido a palitos con orejeras y pompones. Talla única para adulto."),
    ("marisol", "Llaveros de mini mates (3 unidades)", "mates", "30.00", 20, "mate_llaveros",
     "Tres llaveros de calabaza pequeña burilada. Un buen recuerdo para regalar."),
    ("julian", "Olla de barro", "ceramica", "65.00", 6, "olla",
     "Olla de barro para cocinar a leña o a gas. Da a la comida el sabor tradicional de la sierra."),
    ("lucia", "Habas secas 1 kg", "granos", "10.00", 30, "habas",
     "Habas secas de la campaña, ideales para tostar o para sopas."),
    ("teodoro", "Cojín tejido rombo", "textiles", "70.00", 7, "cojin",
     "Funda de cojín tejida en telar, 45 × 45 cm, con relleno incluido."),
    ("felipe", "Jarrón de Quilcas", "ceramica", "90.00", 4, "jarron",
     "Jarrón de cerámica con hojas pintadas a mano. 35 cm de alto."),
    ("rosa", "Poncho tradicional", "textiles", "260.00", 3, "poncho",
     "Poncho de lana de oveja con franjas negras y amarillas, como el que se usa en las fiestas del valle."),
    ("lucia", "Quinua roja 1 kg", "granos", "22.00", 18, "quinua_roja",
     "Quinua roja de grano firme, perfecta para ensaladas. Lavada y lista para cocinar."),
    ("benita", "Individuales tejidos (4 unidades)", "textiles", "60.00", 11, "individuales",
     "Juego de cuatro individuales de mesa tejidos, en rojo, azul, verde y naranja."),
]


class Command(BaseCommand):
    help = "Carga datos de prueba ficticios de FeriaAndina (solo si la base está vacía)."

    def add_arguments(self, parser):
        parser.add_argument("--reiniciar", action="store_true",
                            help="Borra artesanos, productos y pedidos antes de cargar.")

    @transaction.atomic
    def handle(self, *args, **opciones):
        if opciones["reiniciar"]:
            PedidoModelo.objects.all().delete()
            ProductoModelo.objects.all().delete()
            Artesano.objects.all().delete()
            self.stdout.write("Datos anteriores borrados.")
        elif ProductoModelo.objects.exists():
            self.stdout.write("Ya hay productos: no se cargó nada. Usa --reiniciar para empezar de cero.")
            return

        artesanos = {}
        for clave, (nombre, comunidad, oficio, tel) in ARTESANOS.items():
            artesanos[clave], _ = Artesano.objects.get_or_create(
                nombre=nombre, defaults={"comunidad": comunidad, "oficio": oficio, "telefono": tel})

        # Se crean al reves para que el primero de la lista salga primero en el catalogo
        for clave, nombre, cat, precio, stock, foto, desc in reversed(PRODUCTOS):
            p = ProductoModelo(artesano=artesanos[clave], nombre=nombre, categoria=cat,
                               precio=precio, stock=stock, descripcion=desc)
            with open(FOTOS / f"{foto}.jpg", "rb") as f:
                p.foto.save(f"{foto}.jpg", File(f), save=True)

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(artesanos)} artesanos y {len(PRODUCTOS)} productos ficticios."))
