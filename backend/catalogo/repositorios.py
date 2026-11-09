"""
PATRON REPOSITORIO (Repository)
-------------------------------
El resto del sistema pide y guarda Productos "como si estuvieran en
una lista en memoria", sin saber que hay una base de datos detras.
  - ProductoRepositorio      -> el contrato (que se puede hacer)
  - ProductoRepositorioDjango -> como se hace con el ORM de Django
Para pruebas se puede crear otro repositorio en memoria sin tocar
los servicios.
"""
from abc import ABC, abstractmethod

from .dominio import Categoria, Dinero, Producto
from .models import ProductoModelo


class ProductoRepositorio(ABC):
    @abstractmethod
    def obtener(self, producto_id: int) -> Producto: ...

    @abstractmethod
    def listar(self, categoria: str | None = None,
               texto: str | None = None) -> list[Producto]: ...

    @abstractmethod
    def guardar(self, producto: Producto, foto=None) -> Producto: ...


class ProductoRepositorioDjango(ProductoRepositorio):

    # --- Traductores entre el mundo Django y el mundo del dominio ---
    @staticmethod
    def _a_dominio(m: ProductoModelo) -> Producto:
        return Producto(
            id=m.id,
            artesano_id=m.artesano_id,
            nombre=m.nombre,
            descripcion=m.descripcion,
            categoria=Categoria(m.categoria),
            precio=Dinero(m.precio),
            stock=m.stock,
            foto_url=m.foto.url if m.foto else "",
        )

    def obtener(self, producto_id: int) -> Producto:
        return self._a_dominio(ProductoModelo.objects.get(pk=producto_id))

    def listar(self, categoria=None, texto=None) -> list[Producto]:
        consulta = ProductoModelo.objects.filter(stock__gt=0)
        if categoria:
            consulta = consulta.filter(categoria=categoria)
        if texto:
            consulta = consulta.filter(nombre__icontains=texto)
        return [self._a_dominio(m) for m in consulta]

    def guardar(self, producto: Producto, foto=None) -> Producto:
        if producto.id:
            m = ProductoModelo.objects.get(pk=producto.id)
        else:
            m = ProductoModelo()
        m.artesano_id = producto.artesano_id
        m.nombre = producto.nombre
        m.descripcion = producto.descripcion
        m.categoria = producto.categoria.value
        m.precio = producto.precio.monto
        m.stock = producto.stock
        if foto is not None:
            m.foto = foto
        m.save()
        return self._a_dominio(m)
