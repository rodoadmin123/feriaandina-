# Plan oficial de FeriaAndina

> **Fuente de verdad del proyecto.** Resume lo aprobado en el IDL1 (procesos, tecnologías, Scrum) y el IDL2 (DDD, frameworks, prototipo).
> Cualquier cambio de alcance, stack o arquitectura **se decide con la Product Owner (Andrea) y se registra aquí antes de programarlo**.

## 1. Visión

Marketplace que conecta a artesanos y agricultores del **Valle del Mantaro** (Junín, Perú) con compradores de todo el país.
Condición de Andrea: *«los artesanos deben poder subir sus productos desde el celular en el mercado, con una sola mano y sin manual»*.

## 2. Stack aprobado (no se cambia sin decisión registrada)

| Capa | Tecnología | Decidido en |
|---|---|---|
| Back-end | Python 3.11+ · **Django 5.2** · Django REST Framework | IDL1 §3, IDL2 §3 |
| Front-end | **React 18** · Vite 5 · React Router 6 · CSS propio *mobile first* | IDL2 §4 |
| Base de datos | SQLite (prototipo) → **PostgreSQL** (producción) | IDL1 §3 |
| Autenticación | **Firebase Authentication** (celular + código SMS) | IDL1 §3 |
| Pagos | **Culqi** (tarjeta y Yape) | IDL1 §3 |
| Notificaciones | **WhatsApp Business Cloud API** + Firebase Cloud Messaging | IDL1 §3 |
| Mapas / envío | **Google Maps Platform** | IDL1 §3 |
| Facturación | **Nubefact** (OSE/PSE → SUNAT) | IDL1 §3 |
| Imágenes | **Cloudinary** (prototipo: carpeta `media/`) | IDL1 §3 |

**Prohibido sin decisión registrada:** cambiar de framework (Laravel, Express, Spring, Vue, Flutter, Next.js…), agregar librerías de UI (Tailwind, MUI, Bootstrap…), gestores de estado (Redux, Zustand…), ORMs alternativos o una base de datos distinta.

## 3. Arquitectura (DDD)

Contextos delimitados = apps de Django = carpetas de `frontend/src/dominios/`:

| Contexto | Responsabilidad | Estado |
|---|---|---|
| `artesanos` | Quién vende | Prototipo |
| `catalogo` | Qué se vende: publicar, buscar, stock | Prototipo |
| `pedidos` (incluye pagos) | Carrito, pedido, pago, descuento de stock | Prototipo (pago simulado) |
| `envios` | Courier y seguimiento | Pendiente (Sprint 3) |
| `notificaciones` | WhatsApp / push | Pendiente (Sprint 3) |
| `facturacion` | Boleta/factura electrónica | Pendiente (Sprint 4) |

Capas por contexto: **presentación** (`api.py`, `serializers.py`) → **aplicación** (`servicios.py`) → **dominio** (`dominio.py`, Python puro) ← **infraestructura** (`models.py`, `repositorios.py`).
Patrones vigentes: Repositorio, Servicio de aplicación, Fábrica, Estrategia, Objeto de valor.

## 4. Reglas del negocio (invariantes)

1. Nombre de producto ≥ 3 caracteres.
2. Precio (`Dinero`) > 0, en soles, 2 decimales.
3. Todo producto se publica con foto.
4. No se vende más de lo que hay en stock.
5. **El stock solo baja cuando el pago está confirmado** (transacción atómica).
6. Una `LineaDePedido` copia el precio del momento y referencia al producto **solo por id**.

## 5. Product Backlog y estado

| ID | Historia de usuario | Sprint | Estado |
|---|---|---|---|
| HU01 | Como productor, quiero registrarme con mi celular (SMS) | 1 | ⏳ Pendiente (prototipo usa selector «Vendo como») |
| HU02 | Como productor, quiero publicar un producto con foto, precio y stock | 1 | ✅ Prototipo |
| HU03 | Como comprador, quiero ver el catálogo y filtrar por categoría | 1 | ✅ Prototipo |
| HU04 | Como comprador, quiero agregar al carrito y pagar con tarjeta o Yape | 2 | 🟡 Parcial (pago simulado, falta Culqi) |
| HU05 | Como productor, quiero recibir un WhatsApp cuando me compren | 3 | ⏳ Pendiente |
| HU06 | Como comprador, quiero conocer el costo de envío según mi dirección | 3 | ⏳ Pendiente |
| HU07 | Como comprador, quiero recibir mi boleta electrónica | 4 | ⏳ Pendiente |
| HU08 | Como comprador, quiero calificar al productor | 4 | ⏳ Pendiente |

Hoja de ruta: Sprint 2 pagos con Culqi · Sprint 3 WhatsApp + envío con Google Maps · Sprint 4 boleta + calificaciones · Sprint 5 pruebas con usuarios y MVP.

## 6. Definición de «Terminado»

Una historia está terminada solo si:
1. funciona con back y front levantados (`ejecutar-y-verificar`);
2. tiene pruebas que pasan (`python manage.py test`);
3. respeta las capas DDD (`revisar_capas.py` sin errores);
4. se ve y se usa bien en 390 px de ancho, con una mano;
5. se actualizó la tabla de estado de este plan.

## 7. Registro de decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-10 | Django + PostgreSQL + servicios externos (IDL1) | Equipo domina Python; reutilizar APIs probadas |
| 2026-11 | DDD con 3 contextos; React como front-end (IDL2) | Sin instalación para el artesano; componentes reutilizables |
