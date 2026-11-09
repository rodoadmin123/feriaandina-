"""Pruebas del contexto Catálogo: reglas del dominio y API."""
import shutil
import tempfile
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APITestCase

from artesanos.models import Artesano

from .dominio import Categoria, Dinero, ErrorDeDominio, Producto, StockInsuficiente

# Imagen JPEG mínima válida para las pruebas de subida
JPEG_1PX = bytes.fromhex(
    "ffd8ffe000104a46494600010100000100010000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720"
    "222c231c1c2837292c30313434341f27393d38323c2e333432ffc0000b080001000101011100ffc4001f0000010501010101010100000000000000000102030405"
    "060708090a0bffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282"
    "090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495"
    "969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffda0008"
    "010100003f00fbd3ffd9"
)


def producto(**cambios):
    datos = dict(id=1, artesano_id=1, nombre="Manta tejida", descripcion="",
                 categoria=Categoria.TEXTILES, precio=Dinero("180"), stock=5)
    datos.update(cambios)
    return Producto(**datos)


class DineroTests(SimpleTestCase):
    def test_redondea_a_dos_decimales(self):
        self.assertEqual(Dinero("10.5").monto, Decimal("10.50"))

    def test_no_acepta_negativos(self):
        with self.assertRaises(ErrorDeDominio):
            Dinero("-1")

    def test_suma_y_multiplica(self):
        self.assertEqual((Dinero("2.50") + Dinero("1.25")).monto, Decimal("3.75"))
        self.assertEqual(Dinero("38").por(3).monto, Decimal("114.00"))


class ProductoTests(SimpleTestCase):
    def test_nombre_minimo_tres_letras(self):
        with self.assertRaises(ErrorDeDominio):
            producto(nombre="ab")

    def test_precio_mayor_a_cero(self):
        with self.assertRaises(ErrorDeDominio):
            producto(precio=Dinero("0"))

    def test_stock_no_negativo(self):
        with self.assertRaises(ErrorDeDominio):
            producto(stock=-1)

    def test_descontar_stock(self):
        p = producto(stock=5)
        p.descontar_stock(2)
        self.assertEqual(p.stock, 3)

    def test_no_vende_mas_de_lo_que_hay(self):
        with self.assertRaises(StockInsuficiente):
            producto(stock=1).descontar_stock(2)


MEDIA_TEMPORAL = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class ProductosAPITests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.artesano = Artesano.objects.create(
            nombre="Artesana de prueba", comunidad="Hualhuas", oficio="Tejedora", telefono="900000000")

    def datos(self, **cambios):
        d = {"artesano_id": self.artesano.id, "nombre": "Chullo de lana", "precio": "45",
             "stock": "3", "categoria": "textiles",
             "foto": SimpleUploadedFile("chullo.jpg", JPEG_1PX, content_type="image/jpeg")}
        d.update(cambios)
        return d

    def test_publicar_y_aparece_en_catalogo(self):
        r = self.client.post("/api/productos/", self.datos(), format="multipart")
        self.assertEqual(r.status_code, 201, r.data)
        lista = self.client.get("/api/productos/?categoria=textiles").json()
        self.assertEqual([p["nombre"] for p in lista], ["Chullo de lana"])

    def test_publicar_sin_foto_responde_400(self):
        d = self.datos()
        d.pop("foto")
        r = self.client.post("/api/productos/", d, format="multipart")
        self.assertEqual(r.status_code, 400)
        self.assertIn("foto", r.json()["error"])
