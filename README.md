# FeriaAndina – Prototipo del catálogo (IDL2)

Prototipo integrado **Django + React** del marketplace FeriaAndina, que conecta a artesanos y agricultores del Valle del Mantaro con compradores.
Curso: Desarrollo de Aplicaciones – Instituto Continental.

## Arquitectura

- **backend/** – Django 5.2 + Django REST Framework, organizado con **DDD** en tres contextos delimitados:
  - `artesanos` – quién vende
  - `catalogo` – qué se vende (dominio, repositorio, servicios, API)
  - `pedidos` – cómo se compra (agregado Pedido y estrategia de pago)
- **frontend/** – React 18 + Vite + React Router, pensado *mobile first* para usarlo con una sola mano.

Patrones aplicados: Repositorio, Servicio de aplicación, Fábrica, Estrategia y Objeto de valor.

## Cómo ejecutarlo en local

Requisitos: Python 3.11+ y Node.js 18+.

### Terminal 1 – Back-end
```bash
cd backend
python -m venv venv
# Windows:  .\venv\Scripts\Activate.ps1     macOS/Linux:  source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo
python manage.py runserver
```
API: http://localhost:8000/api/productos/

### Terminal 2 – Front-end
```bash
cd frontend
npm install
npm run dev
```
App: http://localhost:5173

## Publicar en internet (Render + Cloudinary)

Así todo el equipo ve y carga datos en **la misma** aplicación.

1. **Cloudinary** (fotos): crea una cuenta gratis en cloudinary.com y copia la **API environment variable** del panel (`cloudinary://...`).
2. **Render**: crea una cuenta en render.com con tu GitHub → **New → Blueprint** → elige este repositorio. Render lee `render.yaml` y crea la web + PostgreSQL.
3. Cuando lo pida, completa: `CLOUDINARY_URL` (lo del paso 1), `DJANGO_ADMIN_USUARIO` y `DJANGO_ADMIN_CLAVE` (tu usuario del panel `/admin/`).
4. Espera el despliegue (5–10 min). El enlace queda como `https://feriaandina-xxxx.onrender.com`.

Al arrancar, el servidor migra la base, carga los 30 productos demo **solo si está vacía** y crea el administrador.
Plan gratis: se duerme tras 15 min sin uso (tarda ~1 min en despertar) y la base PostgreSQL gratuita vence a los 30 días.

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/api/productos/?categoria=&q=` | Catálogo con filtro y búsqueda |
| GET | `/api/productos/{id}/` | Detalle de un producto |
| POST | `/api/productos/` | Publica un producto (FormData con foto) |
| GET | `/api/categorias/` | Categorías del dominio |
| GET | `/api/artesanos/` | Lista de artesanos |
| POST | `/api/pedidos/` | Crea el pedido, cobra y descuenta stock |

## Limitaciones del prototipo

Pagos simulados (sin Culqi real), sin inicio de sesión, SQLite en lugar de PostgreSQL. Los artesanos y productos son datos de prueba ficticios.
