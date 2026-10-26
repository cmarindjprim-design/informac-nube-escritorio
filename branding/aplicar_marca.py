"""Aplica la marca "Informac Nube" al código oficial de Nextcloud Desktop.

Uso: python branding/aplicar_marca.py <carpeta-del-codigo-nextcloud-desktop>
"""
import pathlib
import re
import shutil
import sys

SRC = pathlib.Path(sys.argv[1]).resolve()
HERE = pathlib.Path(__file__).resolve().parent

# Identificadores propios (fijos: no cambiarlos entre versiones o Windows no reconocerá las actualizaciones).
GUIDS = {
    "WIN_SHELLEXT_CONTEXT_MENU_GUID": "{0A5CC74F-230D-4C4E-8BF7-58205DE73908}",
    "WIN_SHELLEXT_OVERLAY_GUID_ERROR": "{96350687-81B2-4274-A817-935911FC6746}",
    "WIN_SHELLEXT_OVERLAY_GUID_OK": "{CD4387C7-57F9-47C4-8A2B-4B9B5D442B32}",
    "WIN_SHELLEXT_OVERLAY_GUID_OK_SHARED": "{09AAABAF-A218-4168-8750-EBB394E23F90}",
    "WIN_SHELLEXT_OVERLAY_GUID_SYNC": "{33680345-B436-4FFA-BB19-DFAF56FFEAD5}",
    "WIN_SHELLEXT_OVERLAY_GUID_WARNING": "{B43C7910-B312-4C5B-BEFA-FA0A0BBFD3DE}",
    "WIN_MSI_UPGRADE_CODE": "E56EDF46-FB32-49C9-BB3D-F0EF25A2055E",
}

VALUES = {
    "APPLICATION_NAME": "Informac Nube",
    "APPLICATION_SHORTNAME": "InformacNube",
    "APPLICATION_EXECUTABLE": "informacnube",
    "APPLICATION_DOMAIN": "informac.cl",
    "APPLICATION_VENDOR": "Informac",
    "APPLICATION_REV_DOMAIN": "cl.informac.nube",
    "APPLICATION_REV_DOMAIN_DBUS": "nube.informac.cl",
    "LINUX_PACKAGE_SHORTNAME": "informacnube",
}


def set_value(text: str, key: str, value: str) -> str:
    """Reemplaza set( KEY "valor" ...) conservando el resto de la línea (CACHE, comentarios)."""
    pattern = re.compile(r'(set\(\s*' + re.escape(key) + r'\s+)"[^"]*"')
    new, n = pattern.subn(lambda m: m.group(1) + '"' + value + '"', text)
    if n == 0:
        raise SystemExit(f"No encontré {key} en NEXTCLOUD.cmake")
    return new


cmake = SRC / "NEXTCLOUD.cmake"
text = cmake.read_text(encoding="utf-8")
for k, v in {**VALUES, **GUIDS}.items():
    text = set_value(text, k, v)
# Sin actualizador automático hacia nextcloud.com, ayuda apuntando a Informac, colores de la marca.
text = set_value(text, "APPLICATION_UPDATE_URL", "")
text = set_value(text, "APPLICATION_HELP_URL", "https://nube.informac.net/apps/informacnube/conectar")
text = set_value(text, "APPLICATION_VIRTUALFILE_SUFFIX", "informacnube")
text = set_value(text, "NEXTCLOUD_BACKGROUND_COLOR", "#22394A")
cmake.write_text(text, encoding="utf-8")
print("NEXTCLOUD.cmake con marca Informac Nube")

theme = SRC / "theme"
icon_svg = HERE / "icon.svg"
icon_png = HERE / "icon.png"
logo_svg = HERE / "logo.svg"
logo_png = HERE / "logo.png"

replace = {
    "colored/Nextcloud-icon.svg": icon_svg,
    "colored/Nextcloud-icon-square.svg": icon_svg,
    "colored/Nextcloud-w10startmenu.svg": icon_svg,
    "colored/Nextcloud-macOS-icon.svg": icon_svg,
    "colored/icons/Nextcloud-icon-win-folder.svg": icon_svg,
    "colored/Nextcloud-w10starttile.png": icon_png,
    "colored/wizard_logo.svg": logo_svg,
    "colored/wizard_logo.png": logo_png,
    "colored/wizard_logo@2x.png": logo_png,
    "colored/wizard-nextcloud.svg": logo_svg,
    "colored/wizard-nextcloud.png": logo_png,
    "colored/wizard-nextcloud@2x.png": logo_png,
    "white/wizard-nextcloud.svg": logo_svg,
    "white/wizard-nextcloud.png": logo_png,
    "white/wizard-nextcloud@2x.png": logo_png,
    "black/wizard-nextcloud.svg": logo_svg,
    "black/wizard-nextcloud.png": logo_png,
    "black/wizard-nextcloud@2x.png": logo_png,
}
for rel, source in replace.items():
    target = theme / rel
    if target.exists():
        shutil.copyfile(source, target)
        print("ícono reemplazado:", rel)
    else:
        print("aviso, no existe (se omite):", rel)


# La compilación busca los íconos por el nombre corto del programa ("InformacNube-..."),
# así que se crea una copia de cada ícono "Nextcloud-..." con el nombre nuevo.
SHORT = VALUES["APPLICATION_SHORTNAME"]
for f in list(theme.rglob("Nextcloud-*")):
    if f.is_file():
        dest = f.with_name(f.name.replace("Nextcloud-", SHORT + "-", 1))
        shutil.copyfile(f, dest)
        print("copia con nombre nuevo:", dest.relative_to(theme))

manifest = theme / "nextcloud.VisualElementsManifest.xml"
if manifest.exists():
    (theme / (VALUES["APPLICATION_EXECUTABLE"] + ".VisualElementsManifest.xml")).write_text(
        manifest.read_text(encoding="utf-8").replace("Nextcloud-", SHORT + "-"), encoding="utf-8")
    print("manifiesto del menú inicio creado")
