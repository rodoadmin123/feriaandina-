"""
Recorre el flujo principal de FeriaAndina y guarda capturas en tamaño celular.
Requisitos: back-end en :8000, front-end en :5173, `pip install playwright` y Chromium.
Uso: python .claude/skills/ejecutar-y-verificar/scripts/capturas.py --salida capturas
"""
import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[4]
FOTO = RAIZ / "backend" / "catalogo" / "demo_fotos" / "chullo.jpg"

p = argparse.ArgumentParser()
p.add_argument("--salida", default="capturas")
p.add_argument("--front", default="http://localhost:5173")
p.add_argument("--api", default="http://localhost:8000")
args = p.parse_args()
OUT = Path(args.salida)
OUT.mkdir(parents=True, exist_ok=True)
F = args.front


def foto(pg, nombre):
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(OUT / f"{nombre}.png"))
    print("captura:", nombre)


with sync_playwright() as pw:
    nav = pw.chromium.launch()
    ctx = nav.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                          is_mobile=True, has_touch=True, locale="es-PE")
    pg = ctx.new_page()

    pg.goto(F + "/"); pg.wait_for_selector(".tarjeta"); foto(pg, "01_catalogo")
    pg.click("text=Textiles"); pg.wait_for_timeout(600); foto(pg, "02_catalogo_filtro")

    pg.click("text=Manta tejida de Hualhuas"); pg.wait_for_selector(".detalle-info")
    stock_antes = pg.inner_text(".stock")
    pg.click("[aria-label=Sumar]"); foto(pg, "03_detalle")
    pg.click("text=Agregar al carrito"); pg.wait_for_selector(".lista-carrito")

    pg.click(".barra-nav >> text=Catálogo"); pg.wait_for_selector(".tarjeta")
    pg.click("text=Café de altura tostado 500 g"); pg.wait_for_selector(".detalle-info")
    pg.click("text=Agregar al carrito"); pg.wait_for_selector(".lista-carrito")
    pg.fill("input[placeholder='Nombre y apellido']", "Comprador de prueba")
    pg.fill("input[placeholder='9XX XXX XXX']", "900000000")
    foto(pg, "04_carrito")
    pg.click("text=Pagar"); pg.wait_for_selector("text=Pago aprobado"); foto(pg, "05_pago_ok")

    pg.click("text=Seguir comprando"); pg.wait_for_selector(".tarjeta")
    pg.click("text=Manta tejida de Hualhuas"); pg.wait_for_selector(".detalle-info")
    stock_despues = pg.inner_text(".stock")

    pg.click(".barra-nav >> text=Vender"); pg.wait_for_selector(".selector-foto")
    pg.wait_for_timeout(600)
    pg.select_option(".vendo-como select", label="Rosa Huamán · Hualhuas")
    foto(pg, "06_vender_vacio")
    pg.fill("input[placeholder='Ej. Chullo de lana']", "Chullo de lana de oveja")
    pg.click(".formulario >> text=Textiles")
    pg.fill("input[placeholder='0.00']", "45")
    pg.click("text=Publicar producto"); pg.wait_for_selector(".aviso-error")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); foto(pg, "07_vender_error")
    pg.set_input_files("[data-testid=foto]", str(FOTO))
    for _ in range(2):
        pg.click("[aria-label=Sumar]")
    pg.evaluate("window.scrollTo(0, 0)"); foto(pg, "08_vender_lleno")
    pg.click("text=Publicar producto"); pg.wait_for_selector("text=¡Producto publicado!")
    foto(pg, "09_publicado")
    pg.click(".barra-nav >> text=Catálogo"); pg.wait_for_selector(".tarjeta"); foto(pg, "10_catalogo_nuevo")

    esc = nav.new_context(viewport={"width": 1100, "height": 760}, device_scale_factor=1.5).new_page()
    esc.goto(args.api + "/api/productos/?categoria=textiles"); foto(esc, "11_api")
    nav.close()

print(f"\nStock de la manta: antes «{stock_antes}» → después «{stock_despues}» (debe bajar en 2)")
