"""Pruebas del contexto Pedidos: agregado y regla «el stock baja solo al pagar»."""
from django.test import SimpleTestCase
from rest_framework.test import APITestCase

from artesanos.models import Artesano
from catalogo.dominio import Categoria, Dinero, ErrorDeDominio, Producto
from catalogo.models import ProductoModelo

from .dominio import EstadoPedido, Pedido


class PedidoTests(SimpleTestCase):
    def setUp(self):
        self.manta = Producto(1, 1, "Manta tejida", "", Categoria.TEXTILES, Dinero("180"), 5)
        self.cafe = Producto(2, 1, "Café 500 g", "", Categoria.CAFE, Dinero("38"), 10)

    def test_total_suma_las_lineas(self):
        pedido = Pedido(None, "Comprador", "900000000", "yape")
        pedido.agregar(self.manta, 2)
        pedido.agregar(self.cafe, 1)
        self.assertEqual(str(pedido.total), "S/ 398.00")

    def test_no_agrega_sin_stock(self):
        with self.assertRaises(ErrorDeDominio):
            Pedido(None, "C", "9", "yape").agregar(self.manta, 6)

    def test_pedido_vacio_no_se_paga(self):
        with self.assertRaises(ErrorDeDominio):
            Pedido(None, "C", "9", "yape").marcar_pagado("X")


class PedidosAPITests(APITestCase):
    def setUp(self):
        a = Artesano.objects.create(nombre="A", comunidad="Aco", oficio="Ceramista", telefono="9")
        self.p = ProductoModelo.objects.create(artesano=a, nombre="Cántaro", categoria="ceramica",
                                               precio="70", stock=5)

    def pedir(self, cantidad, metodo="yape"):
        return self.client.post("/api/pedidos/", {
            "comprador": "Comprador", "telefono": "900000000", "metodo_pago": metodo,
            "items": [{"producto_id": self.p.id, "cantidad": cantidad}]}, format="json")

    def test_pago_descuenta_stock(self):
        r = self.pedir(2)
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(r.json()["estado"], EstadoPedido.PAGADO.value)
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock, 3)

    def test_sin_stock_no_cobra_ni_descuenta(self):
        r = self.pedir(9)
        self.assertEqual(r.status_code, 400)
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock, 5)

    def test_metodo_de_pago_invalido(self):
        r = self.pedir(1, metodo="trueque")
        self.assertEqual(r.status_code, 400)
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock, 5)
