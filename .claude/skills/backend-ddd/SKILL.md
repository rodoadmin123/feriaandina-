---
name: backend-ddd
description: Cómo agregar o cambiar funcionalidad en el back-end Django de FeriaAndina respetando DDD (dominio → repositorio → servicio → API → urls) y sus patrones. Úsalo para cualquier cambio en backend/: nuevas entidades, reglas del negocio, casos de uso, endpoints o un contexto nuevo (envios, notificaciones, facturacion).
---

# Back-end con DDD

Antes de empezar, pasa por `guardian-del-plan`.

## Mapa de capas (por cada app/contexto)

| Archivo | Capa | Puede importar | Contiene |
|---|---|---|---|
| `dominio.py` | Dominio | solo librería estándar y otros `dominio.py` | Entidades, objetos de valor, reglas, `ErrorDeDominio` |
| `repositorios.py` | Infraestructura | `models.py`, `dominio.py` | Contrato (ABC) + implementación Django; traduce modelo ↔ entidad |
| `models.py` | Infraestructura | Django | Solo persistencia; sin reglas |
| `servicios.py` | Aplicación | dominio, repositorios, `transaction` | Un caso de uso por clase con `ejecutar()`; fábricas |
| `api.py` + `serializers.py` | Presentación | servicios, DRF | Traducir HTTP ↔ servicio; capturar `ErrorDeDominio` → 400 |
| `config/urls.py` | Presentación | `api.py` | Rutas `/api/<recurso>/` agrupadas por contexto |

## Receta: nueva funcionalidad

1. **Dominio primero.** Escribe o ajusta la entidad / objeto de valor en `dominio.py`. Las invariantes van en `__post_init__` o en métodos con nombre del negocio (`descontar_stock`, `marcar_pagado`). Errores con `ErrorDeDominio` y mensajes en español claro.
2. **Prueba del dominio** en `<app>/tests.py` usando `SimpleTestCase` (sin base de datos): caso válido + cada regla violada.
3. **Persistencia.** Si cambia la forma de los datos: `models.py` → `python manage.py makemigrations <app>` → actualiza los traductores `_a_dominio` y `guardar` del repositorio.
4. **Caso de uso** en `servicios.py`: recibe datos simples, usa la Fábrica, el Repositorio y, si toca varias entidades, `@transaction.atomic`.
5. **API.** Vista delgada en `api.py`, serializer de salida que lee la entidad (no el modelo), ruta en `config/urls.py`.
6. **Prueba de integración** con `APITestCase`: respuesta 201/200 y 400 con el mensaje de dominio.
7. Ejecuta `python manage.py test` y `python ../.claude/skills/backend-ddd/scripts/revisar_capas.py`.

## Receta: contexto nuevo (solo si su sprint está activo en el plan)

```bash
cd backend && python manage.py startapp <contexto>
```
Agrega la app a `INSTALLED_APPS` (bajo «Contextos delimitados»), crea `dominio.py`, `repositorios.py`, `servicios.py`, `api.py`, `serializers.py` y borra `views.py`.
Entre contextos **referencia por id**, nunca con ForeignKey hacia otro agregado salvo `Artesano` (ya establecido).

## Integraciones externas del plan

Van detrás de una **interfaz en el dominio o en la aplicación** (patrón Estrategia/Adaptador), igual que `pedidos/pagos.py`:
- Culqi → nueva clase que implementa `MetodoPago`; claves en variables de entorno, nunca en el código.
- WhatsApp, Google Maps, Nubefact, Cloudinary → `<contexto>/adaptadores.py` con una clase simulada para desarrollo y la real para producción.

## No hagas

- Reglas en serializers, vistas o señales de Django.
- `ModelViewSet` genéricos que salten el servicio (para escribir siempre pasa por `servicios.py`).
- Devolver el modelo de Django directo al front; siempre la entidad serializada.
