"""Ajusta la receta de empaquetado (Craft) para que el instalador sea "Informac Nube".

Uso: python branding/parchar_empaquetado.py <carpeta-craft-del-objetivo>
Busca la receta nextcloud-client.py descargada por Craft y:
- agrega "import os" (falta en la receta oficial y el empaquetado se cae),
- cambia nombre, empresa y ejecutable del instalador.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
recipes = list(root.rglob("craft-blueprints-nextcloud/nextcloud-client/nextcloud-client.py"))
if not recipes:
    raise SystemExit("No encontré la receta nextcloud-client.py de Craft")

for recipe in recipes:
    text = recipe.read_text(encoding="utf-8")
    if "\nimport os\n" not in text:
        text = text.replace("import info\n", "import info\nimport os\n", 1)
    replacements = {
        'self.defines["appname"] = "nextcloud"': 'self.defines["appname"] = "informacnube"',
        'self.defines["company"] = "Nextcloud GmbH"': 'self.defines["company"] = "Informac"',
        'self.applicationExecutable = "nextcloud"': 'self.applicationExecutable = "informacnube"\n'
        '        self.defines["productname"] = "Informac Nube"\n'
        '        self.defines["website"] = "https://informac.cl"',
    }
    for old, new in replacements.items():
        if old not in text:
            print("aviso, no encontré:", old)
        text = text.replace(old, new)
    recipe.write_text(text, encoding="utf-8")
    print("receta ajustada:", recipe)
