"""
Revisa que el back-end respete las capas DDD de FeriaAndina.
Uso (desde backend/):  python ../.claude/skills/backend-ddd/scripts/revisar_capas.py
Sale con codigo 1 si encuentra violaciones.
"""
import ast
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4] / "backend"
CONTEXTOS = [p.parent for p in RAIZ.glob("*/apps.py")]

PROHIBIDO = {
    "dominio.py": ("django", "rest_framework"),            # dominio puro
    "api.py": ("models",),                                   # vistas no tocan modelos para escribir
    "serializers.py": (),
}


def importaciones(archivo: Path):
    arbol = ast.parse(archivo.read_text(encoding="utf-8"))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                yield nodo.lineno, a.name
        elif isinstance(nodo, ast.ImportFrom):
            modulo = ("." * nodo.level) + (nodo.module or "")
            yield nodo.lineno, modulo


errores = []
avisos = []
for ctx in CONTEXTOS:
    dominio = ctx / "dominio.py"
    if dominio.exists():
        for linea, mod in importaciones(dominio):
            if mod.split(".")[0] in PROHIBIDO["dominio.py"]:
                errores.append(f"{dominio.relative_to(RAIZ)}:{linea} importa '{mod}' (el dominio debe ser Python puro)")
    api = ctx / "api.py"
    if api.exists():
        texto = api.read_text(encoding="utf-8")
        for linea, mod in importaciones(api):
            if mod.endswith("models"):
                avisos.append(f"{api.relative_to(RAIZ)}:{linea} importa modelos; úsalos solo para consultas/404, nunca para escribir")
        for patron in (".save(", ".objects.create(", ".delete("):
            if patron in texto:
                errores.append(f"{api.relative_to(RAIZ)} usa '{patron}' (escribir datos es trabajo del servicio/repositorio)")
    if (ctx / "views.py").exists() and (ctx / "api.py").exists():
        avisos.append(f"{ctx.name}/views.py sobra: la presentación va en api.py")

for a in avisos:
    print("AVISO  ", a)
for e in errores:
    print("ERROR  ", e)
print(f"\nContextos revisados: {', '.join(c.name for c in CONTEXTOS)}")
print("OK: capas DDD respetadas." if not errores else f"{len(errores)} violación(es) de capas.")
sys.exit(1 if errores else 0)
