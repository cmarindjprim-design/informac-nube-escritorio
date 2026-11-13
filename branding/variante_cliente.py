"""Variante del programa para un cliente: pone el logo del cliente en las pantallas del programa.

Uso: python branding/variante_cliente.py <cliente>
Hoy existe la variante "sigma". El programa sigue siendo "Informac Nube" (mismo ejecutable, mismo
servidor fijo); solo cambian el logo de las pantallas de ingreso y el nombre del instalador.
"""
import base64
import io
import pathlib
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
CLIENTES = {
    "sigma": {
        "logo": "https://isigma.cl/wp-content/uploads/2022/07/logo-sigma-1.png",
        "texto": "Nube",
        "pie": "por Informac",
    },
}

cliente = sys.argv[1].strip().lower()
if cliente not in CLIENTES:
    raise SystemExit(f"Cliente desconocido: {cliente}")
c = CLIENTES[cliente]

req = urllib.request.Request(c["logo"], headers={"User-Agent": "Mozilla/5.0 (Informac build)"})
data = urllib.request.urlopen(req, timeout=60).read()
logo = Image.open(io.BytesIO(data)).convert("RGBA")
bbox = logo.getbbox()
if bbox:
    logo = logo.crop(bbox)

W, H = 720, 140
lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
alto = H - 16
ancho = round(logo.width * alto / logo.height)
if ancho > 430:
    ancho = 430
    alto = round(logo.height * ancho / logo.width)
logo = logo.resize((ancho, alto), Image.LANCZOS)
lienzo.paste(logo, (0, (H - alto) // 2), logo)

fuentes = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
fuentes_n = [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]


def fuente(lista, tam):
    for f in lista:
        try:
            return ImageFont.truetype(f, tam)
        except OSError:
            pass
    return ImageFont.load_default()


d = ImageDraw.Draw(lienzo)
x = ancho + 28
d.line([(x - 14, 22), (x - 14, H - 22)], fill=(220, 227, 233, 255), width=3)
d.text((x, 18), c["texto"], font=fuente(fuentes, 64), fill=(34, 57, 74, 255))
d.text((x + 2, 92), c["pie"], font=fuente(fuentes_n, 30), fill=(196, 18, 47, 255))

png = HERE / "logo.png"
lienzo.save(png)
b64 = base64.b64encode(png.read_bytes()).decode()
(HERE / "logo.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="360" height="70" '
    f'viewBox="0 0 360 70"><image width="360" height="70" xlink:href="data:image/png;base64,{b64}"/></svg>',
    encoding="utf-8")
print(f"Logo de {cliente} aplicado: {png} ({lienzo.size})")
