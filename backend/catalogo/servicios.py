"""
CONTEXTO: CATALOGO  -  capa de APLICACION
-----------------------------------------
PATRON SERVICIO DE APLICACION (Service Layer): cada caso de uso del
negocio es una clase con un solo metodo "ejecutar". La vista (API)
no tiene reglas: solo llama al servicio.

PATRON FABRICA (Factory): ProductoFabrica arma un Producto valido a
partir de los datos sueltos que llegan del formulario del celular.
"""
from artesanos.models import Artesano

from .dominio import Categoria, Dinero, ErrorDeDominio, Producto
from .repositorios import ProductoRepositorio, ProductoRepositorioDjango


class ProductoFabrica:
    @staticmethod
    def crear(artesano_id, nombre, precio, stock, categoria,
              descripcion="") -> Producto:
        try:
            stock = int(stock)
        except (TypeError, ValueError):
            raise ErrorDeDominio("El stock debe ser un numero entero.")
        return Producto(
            id=None,
            artesano_id=int(artesano_id),
            nombre=nombre or "",
            descripcion=descripcion or "",
            categoria=Categoria.desde_texto(categoria),
            precio=Dinero(precio),
            stock=stock,
        )


class PublicarProducto:
    """Caso de uso del IDL1, paso 3: 'El productor publica un producto'."""

    def __init__(self, repositorio: ProductoRepositorio | None = None):
        # Inyeccion de dependencias: se puede pasar otro repositorio
        self.repositorio = repositorio or ProductoRepositorioDjango()

    def ejecutar(self, datos: dict, foto=None) -> Producto:
        if not Artesano.objects.filter(pk=datos.get("artesano_id")).exists():
            raise ErrorDeDominio("El artesano no esta registrado.")
        if foto is None:
            raise ErrorDeDominio("Toma al menos una foto del producto.")
        producto = ProductoFabrica.crear(**datos)
        return self.repositorio.guardar(producto, foto=foto)


class ConsultarCatalogo:
    """Caso de uso del IDL1, paso 5: 'El comprador busca y filtra'."""

    def __init__(self, repositorio: ProductoRepositorio | None = None):
        self.repositorio = repositorio or ProductoRepositorioDjango()

    def ejecutar(self, categoria=None, texto=None) -> list[Producto]:
        return self.repositorio.listar(categoria, texto)
