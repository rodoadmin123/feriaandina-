"""
CONTEXTO: CATALOGO  -  capa de DOMINIO
--------------------------------------
Aqui viven las reglas del negocio en Python puro (sin Django).
Si manana cambiamos de framework o de base de datos, este archivo
no cambia. Eso es lo central de Domain-Driven Design (DDD).
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum


class ErrorDeDominio(Exception):
    """Una regla del negocio no se cumple."""


class StockInsuficiente(ErrorDeDominio):
    pass


# ------------------------------------------------------------------
# OBJETO DE VALOR (Value Object): Dinero
# No tiene identidad propia: S/ 85.00 es igual a cualquier otro
# S/ 85.00. Es inmutable (frozen=True) y se valida a si mismo.
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Dinero:
    monto: Decimal
    moneda: str = "PEN"

    def __post_init__(self):
        try:
            valor = Decimal(str(self.monto)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            raise ErrorDeDominio("El precio debe ser un numero.")
        if valor < 0:
            raise ErrorDeDominio("El precio no puede ser negativo.")
        object.__setattr__(self, "monto", valor)

    def __add__(self, otro: "Dinero") -> "Dinero":
        return Dinero(self.monto + otro.monto, self.moneda)

    def por(self, cantidad: int) -> "Dinero":
        return Dinero(self.monto * cantidad, self.moneda)

    def __str__(self):
        return f"S/ {self.monto:.2f}"


# ------------------------------------------------------------------
# OBJETO DE VALOR: Categoria (lista cerrada del lenguaje ubicuo)
# ------------------------------------------------------------------
class Categoria(str, Enum):
    TEXTILES = "textiles"
    CERAMICA = "ceramica"
    MATES = "mates"            # mates burilados
    CAFE = "cafe"
    GRANOS = "granos"          # quinua, kiwicha, maiz

    @classmethod
    def desde_texto(cls, texto: str) -> "Categoria":
        try:
            return cls(texto)
        except ValueError:
            raise ErrorDeDominio(f"Categoria desconocida: {texto}")


# ------------------------------------------------------------------
# ENTIDAD y RAIZ DE AGREGADO: Producto
# Tiene identidad (id). Protege sus propias reglas (invariantes):
# nombre obligatorio, precio > 0, stock nunca negativo.
# ------------------------------------------------------------------
@dataclass
class Producto:
    id: int | None
    artesano_id: int
    nombre: str
    descripcion: str
    categoria: Categoria
    precio: Dinero
    stock: int
    foto_url: str = ""

    def __post_init__(self):
        self.nombre = self.nombre.strip()
        if len(self.nombre) < 3:
            raise ErrorDeDominio("El nombre debe tener al menos 3 letras.")
        if self.precio.monto <= 0:
            raise ErrorDeDominio("El precio debe ser mayor a 0.")
        if self.stock < 0:
            raise ErrorDeDominio("El stock no puede ser negativo.")

    def hay_stock(self, cantidad: int) -> bool:
        return 0 < cantidad <= self.stock

    def descontar_stock(self, cantidad: int) -> None:
        """Regla del IDL1: el stock baja solo cuando se confirma el pago."""
        if not self.hay_stock(cantidad):
            raise StockInsuficiente(
                f"Solo quedan {self.stock} unidades de {self.nombre}.")
        self.stock -= cantidad
