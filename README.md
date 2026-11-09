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
