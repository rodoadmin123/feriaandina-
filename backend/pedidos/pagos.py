"""
PATRON ESTRATEGIA (Strategy)
----------------------------
Cada medio de pago es una "estrategia" con el mismo metodo cobrar().
El servicio de pedidos no sabe si se paga con Yape o tarjeta: solo
llama a cobrar(). Para agregar Plin, se crea otra clase y listo.
En el prototipo los cobros son SIMULADOS; en produccion se conectan
a la pasarela Culqi elegida en el IDL1.
"""
import uuid
from abc import ABC, abstractmethod

from catalogo.dominio import Dinero, ErrorDeDominio


class MetodoPago(ABC):
    @abstractmethod
    def cobrar(self, monto: Dinero, referencia: str) -> str:
        """Devuelve el codigo de la operacion aprobada."""


class PagoYape(MetodoPago):
    def cobrar(self, monto, referencia):
        return "YAPE-" + uuid.uuid4().hex[:8].upper()


class PagoTarjeta(MetodoPago):
    def cobrar(self, monto, referencia):
        return "CULQI-" + uuid.uuid4().hex[:8].upper()


# Fabrica sencilla que elige la estrategia segun el texto recibido
METODOS = {"yape": PagoYape, "tarjeta": PagoTarjeta}


def obtener_metodo(nombre: str) -> MetodoPago:
    if nombre not in METODOS:
        raise ErrorDeDominio(f"Metodo de pago no valido: {nombre}")
    return METODOS[nombre]()
