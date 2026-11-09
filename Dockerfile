# =============================================================
# FeriaAndina: imagen para el servidor (Render)
# Paso 1 compila React, paso 2 instala Django y le entrega React.
# =============================================================

# ---------- 1. Front-end: React -> archivos estaticos ----------
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---------- 2. Back-end: Django + React compilado ----------
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DEBUG=0
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=frontend /app/dist ./frontend_dist
RUN python manage.py collectstatic --noinput
COPY iniciar.sh ./
RUN chmod +x iniciar.sh
CMD ["./iniciar.sh"]
