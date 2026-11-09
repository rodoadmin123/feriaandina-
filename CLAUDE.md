# FeriaAndina – instrucciones para agentes

Marketplace de artesanos del Valle del Mantaro. Prototipo **Django 5.2 + DRF** (`backend/`) y **React 18 + Vite** (`frontend/`), diseñado con **DDD**.

## Regla número 1: no salirse del plan

- `docs/PLAN.md` es la **fuente de verdad**: stack, contextos, reglas del negocio, backlog y estado.
- **Antes de cualquier tarea** usa el skill `guardian-del-plan`. Si la tarea no encaja en el plan (otro framework, una librería nueva, una funcionalidad fuera del backlog), **detente y pregunta al usuario**; no la implementes «de paso».
- **Al terminar**, actualiza la tabla de estado de `docs/PLAN.md`.

## Skills del proyecto

| Skill | Cuándo usarlo |
|---|---|
| `guardian-del-plan` | Siempre, al empezar y al terminar una tarea |
| `backend-ddd` | Cualquier cambio en `backend/` (modelo, regla, servicio, endpoint) |
| `pantalla-movil` | Cualquier pantalla o componente en `frontend/` |
| `ejecutar-y-verificar` | Levantar el proyecto, correr pruebas, tomar capturas en tamaño celular |

## Convenciones

- **Idioma:** español en nombres de dominio, variables, mensajes al usuario y commits (lenguaje ubicuo: Artesano, Producto, Pedido, Dinero, Categoria…). Sin tildes en identificadores de código; con tildes en textos visibles.
- **Dominio puro:** `*/dominio.py` no importa Django ni DRF.
- **Vistas delgadas:** `api.py` solo traduce HTTP ↔ servicio; las reglas viven en el dominio o en `servicios.py`.
- **Errores de negocio:** se lanzan como `ErrorDeDominio` y la API responde `400 {"error": "mensaje claro"}`.
- **Front-end por dominio:** `frontend/src/dominios/<contexto>/{api.js,componentes/,paginas/}`; lo reutilizable va en `frontend/src/compartido/`.
- **Datos:** los artesanos y productos de `cargar_demo` son ficticios; nunca uses datos personales reales.
- **Servidor compartido (Render):** la base de datos es del equipo. Nunca ejecutes `--reiniciar`, borres datos ni cambies variables de entorno sin pedirlo el usuario. Las claves (Cloudinary, admin) van en el panel de Render, jamás en el código.

## Comandos rápidos

```bash
# back-end
cd backend && python manage.py migrate && python manage.py cargar_demo && python manage.py runserver
python manage.py cargar_demo --reiniciar   # borra y recarga los 30 productos demo (solo en local)
python manage.py test
python ../.claude/skills/backend-ddd/scripts/revisar_capas.py
# front-end
cd frontend && npm install && npm run dev      # http://localhost:5173 (proxy a :8000)
npm run build
```
