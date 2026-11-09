---
name: ejecutar-y-verificar
description: Levanta FeriaAndina (Django + React), carga los datos de prueba, corre las pruebas y la revisión de capas, y toma capturas en tamaño celular para comprobar o documentar el trabajo (también para los informes IDL). Úsalo para verificar cualquier cambio antes de darlo por terminado o cuando pidan capturas de las pantallas.
---

# Ejecutar y verificar

## 1. Preparar (solo la primera vez)

```bash
cd backend
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1   ·   macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo
cd ../frontend && npm install
```

## 2. Pruebas automáticas (Definición de Terminado, puntos 2 y 3)

```bash
cd backend
python manage.py test
python ../.claude/skills/backend-ddd/scripts/revisar_capas.py
cd ../frontend && npm run build
```
Las tres deben terminar sin errores. Si una prueba falla, se arregla el código, no la prueba (salvo que la regla haya cambiado en `docs/PLAN.md`).

## 3. Levantar los servidores

En dos terminales (o en segundo plano):
```bash
cd backend && python manage.py runserver 8000
cd frontend && npm run dev -- --port 5173
```
Comprueba: `http://localhost:8000/api/productos/` devuelve JSON y `http://localhost:5173` muestra el catálogo.
Si tocaste datos de prueba: `python manage.py cargar_demo` reinicia artesanos y productos.

## 4. Capturas en tamaño celular

Con los dos servidores levantados y Playwright disponible (`pip install playwright` y `playwright install chromium` si no está):
```bash
python .claude/skills/ejecutar-y-verificar/scripts/capturas.py --salida capturas
```
Recorre el flujo del plan y guarda PNG numerados en 390 × 844 @2x:
`01_catalogo` · `02_catalogo_filtro` · `03_detalle` · `04_carrito` · `05_pago_ok` · `06_vender_vacio` · `07_vender_error` · `08_vender_lleno` · `09_publicado` · `10_catalogo_nuevo` · `11_api`.
Al final imprime el stock antes y después del pago, que debe bajar. Ejecuta `cargar_demo` antes, para partir de datos limpios.

**Revisa las capturas** (ábrelas): barra inferior sin tapar contenido, botón principal visible, textos sin cortes, errores en rojo legibles.

## 5. Para informes académicos (IDL)

- Usa las capturas de la carpeta de salida y describe cada ventana con: objetivo, elementos, integración (endpoint) y paso del proceso del IDL1.
- Aclara en el informe que los datos son de prueba ficticios.
- Las capturas propias de quien entrega, tomadas en su PC o celular, valen más como evidencia que las generadas por un agente.
