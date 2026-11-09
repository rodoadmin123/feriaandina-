---
name: guardian-del-plan
description: Verifica que una tarea de FeriaAndina encaje en el plan oficial (docs/PLAN.md) antes de programar, y actualiza el estado del backlog al terminar. Úsalo SIEMPRE al empezar y al cerrar cualquier tarea en este repositorio, y cuando alguien proponga un framework, librería, funcionalidad o cambio de arquitectura.
---

# Guardián del plan

El plan de FeriaAndina ya fue aprobado (IDL1 + IDL2). Este skill evita que el proyecto se desvíe.

## Al EMPEZAR una tarea

1. Lee `docs/PLAN.md` completo.
2. Clasifica la tarea con esta tabla:

| La tarea… | Acción |
|---|---|
| Implementa o corrige una HU del backlog (HU01–HU08) | ✅ Adelante. Anota qué HU es. |
| Mejora algo ya hecho sin cambiar stack ni alcance (bug, estilo, prueba, refactor dentro de las capas) | ✅ Adelante. |
| Agrega una funcionalidad que **no está** en el backlog | ⛔ Detente. Pregunta al usuario si se agrega como nueva HU (con sprint) antes de programar. |
| Cambia el stack (otro framework, BD, librería de UI, gestor de estado, ORM) | ⛔ Detente. Explica el costo frente al plan y pide decisión explícita. |
| Rompe una regla del negocio (sección 4 del plan) | ⛔ No lo hagas. Explica la regla. |
| Toca un contexto «Pendiente» antes de su sprint | ⚠️ Pregunta si se adelanta el sprint. |

3. Antes de escribir código, di en una línea: **«Tarea: … · HU: … · Contexto(s): … · Skill a usar: …»**.

## Señales de desvío (frena y pregunta)

- `npm install` o `pip install` de algo que no está en `package.json` / `requirements.txt`.
- Lógica de negocio en `api.py`, en serializers o en componentes de React (por ejemplo, calcular stock o totales «oficiales» en el front).
- Importar `django` dentro de un `dominio.py`.
- Crear carpetas fuera de la estructura por dominio.
- Datos personales reales en fixtures o capturas.

## Al TERMINAR una tarea

1. Comprueba la **Definición de Terminado** (sección 6 del plan) con el skill `ejecutar-y-verificar`.
2. Actualiza la tabla **Product Backlog y estado** de `docs/PLAN.md` (⏳ → 🟡 → ✅) con una nota corta.
3. Si se tomó una decisión nueva aprobada por el usuario, agrégala al **Registro de decisiones** con fecha.
4. Resume al usuario: qué HU avanzó, qué falta y si algo quedó fuera del plan.
