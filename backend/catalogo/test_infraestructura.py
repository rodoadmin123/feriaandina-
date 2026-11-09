"""Pruebas de infraestructura: carga de datos demo, administrador y adaptador de Cloudinary."""
import os
import shutil
import tempfile
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings

from artesanos.models import Artesano
from catalogo.models import ProductoModelo
from config.almacenamiento import AlmacenamientoCloudinary

MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA)
class CargarDemoTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA, ignore_errors=True)
        super().tearDownClass()

    def test_carga_30_productos_y_no_borra_lo_existente(self):
        call_command("cargar_demo", stdout=StringIO())
        self.assertEqual(ProductoModelo.objects.count(), 30)
        self.assertEqual(Artesano.objects.count(), 10)
        # Un producto subido por el equipo despues de la carga
        ProductoModelo.objects.create(artesano=Artesano.objects.first(), nombre="Subido por el equipo",
                                      categoria="textiles", precio="10", stock=1)
        call_command("cargar_demo", stdout=StringIO())  # segunda vez: no toca nada
        self.assertTrue(ProductoModelo.objects.filter(nombre="Subido por el equipo").exists())
        self.assertEqual(ProductoModelo.objects.count(), 31)

    def test_reiniciar_borra_y_vuelve_a_cargar(self):
        call_command("cargar_demo", stdout=StringIO())
        call_command("cargar_demo", "--reiniciar", stdout=StringIO())
        self.assertEqual(ProductoModelo.objects.count(), 30)


class CrearAdminTests(TestCase):
    @mock.patch.dict(os.environ, {"DJANGO_ADMIN_USUARIO": "equipo", "DJANGO_ADMIN_CLAVE": "clave-segura-123"})
    def test_crea_una_sola_vez(self):
        call_command("crear_admin", stdout=StringIO())
        call_command("crear_admin", stdout=StringIO())
        usuarios = get_user_model().objects.filter(username="equipo")
        self.assertEqual(usuarios.count(), 1)
        self.assertTrue(usuarios.first().is_superuser)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_sin_variables_no_crea(self):
        call_command("crear_admin", stdout=StringIO())
        self.assertEqual(get_user_model().objects.count(), 0)


class AlmacenamientoCloudinaryTests(SimpleTestCase):
    @mock.patch("config.almacenamiento.cloudinary.uploader.upload")
    def test_sube_y_devuelve_nombre_con_formato(self, subir):
        subir.return_value = {"public_id": "feriaandina/productos/chullo_ab12", "format": "jpg"}
        nombre = AlmacenamientoCloudinary().save("productos/chullo.jpg", ContentFile(b"x", name="chullo.jpg"))
        self.assertEqual(nombre, "feriaandina/productos/chullo_ab12.jpg")
        self.assertEqual(subir.call_args.kwargs["public_id"], "feriaandina/productos/chullo")

    @mock.patch.dict(os.environ, {"CLOUDINARY_URL": "cloudinary://123:abc@demo-nube"})
    def test_url_segura_y_optimizada(self):
        import cloudinary
        cloudinary.reset_config()
        url = AlmacenamientoCloudinary().url("feriaandina/productos/chullo_ab12.jpg")
        self.assertTrue(url.startswith("https://res.cloudinary.com/demo-nube/image/upload/"))
        self.assertIn("q_auto", url)
        self.assertTrue(url.endswith("feriaandina/productos/chullo_ab12.jpg"))
