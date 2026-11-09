#!/bin/sh
# Se ejecuta cada vez que arranca el servidor en Render.
set -e
python manage.py migrate --noinput
python manage.py cargar_demo        # solo carga si la base esta vacia: no borra datos del equipo
python manage.py crear_admin        # crea el administrador si no existe
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
