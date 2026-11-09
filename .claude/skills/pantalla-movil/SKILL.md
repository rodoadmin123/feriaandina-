---
name: pantalla-movil
description: Cómo crear o modificar pantallas y componentes React de FeriaAndina con las reglas «una sola mano y sin manual» y la estructura por dominio (DDD). Úsalo para cualquier cambio en frontend/: pantallas nuevas, formularios, componentes, estilos o llamadas a la API.
---

# Pantalla móvil (React)

Antes de empezar, pasa por `guardian-del-plan`. El stack es fijo: React 18 + Vite + React Router + CSS propio (`src/estilos.css`). **No** agregues Tailwind, MUI, Redux, Axios ni similares.

## Dónde va cada cosa

```
src/dominios/<contexto>/api.js          funciones que llaman a /api/... (usan pedirApi de compartido/api.js)
src/dominios/<contexto>/componentes/    piezas propias del contexto (TarjetaProducto, SelectorFoto…)
src/dominios/<contexto>/paginas/        pantallas completas (una por ruta)
src/compartido/componentes/             reutilizables entre contextos (Contador, Icono, BarraNavegacion)
src/App.jsx                             registrar la ruta, con un comentario del contexto
```
Nombres de componentes en español y del lenguaje ubicuo (`ResumenPedido`, no `OrderSummary`).

## Reglas «una sola mano y sin manual» (obligatorias)

1. Diseña primero para **390 px** de ancho; el contenedor máximo es 480 px.
2. La **acción principal** va en `.accion-fija` (abajo, sobre la barra de navegación) con `.boton-principal`. La pantalla usa `.pantalla-con-accion`.
3. Objetivos táctiles de **≥ 48 px**; botones principales de 56 px (`--alto-boton`).
4. Máximo **5 datos** por formulario. Preguntas en lenguaje simple («¿Qué vendes?», «¿Cuántos tienes?»).
5. Opciones cortas como **fichas** (`.chip`), no como `<select>`; cantidades con `<Contador>` en vez de escribir.
6. Teclado correcto: `inputMode="decimal"` para precios, `inputMode="tel"` para celulares; fotos con `accept="image/*" capture="environment"`.
7. Estados siempre visibles: cargando, vacío (`.vacio`) y error (`.aviso.aviso-error` con el mensaje que manda el back-end).
8. Textos visibles en español peruano, con tildes; montos con `soles()` de `compartido/api.js`.
9. Colores y medidas solo con las variables de `:root` (`--terracota`, `--maiz`, `--radio`…).

## Integración con el back-end

- Toda llamada pasa por `pedirApi()` (lanza `Error` con el mensaje de dominio).
- Formularios con foto → `FormData`; el resto → JSON.
- El front **no decide reglas del negocio**: puede limitar la interfaz (por ejemplo, el máximo del contador = stock), pero la verdad la confirma la API.
- El estado compartido entre pantallas usa React Context (como `CarritoContexto`); no agregues librerías de estado.

## Antes de dar por terminado

1. `npm run build` sin errores.
2. Usa `ejecutar-y-verificar` para recorrer la pantalla en 390 × 844 y revisar la captura: nada tapado por la barra inferior, el botón principal alcanzable y los textos sin cortarse.
