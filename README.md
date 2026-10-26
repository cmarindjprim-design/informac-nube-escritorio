# Informac Nube — programa de escritorio para Windows

Versión con la marca **Informac Nube** del programa oficial y de código abierto
[Nextcloud Desktop](https://github.com/nextcloud/desktop) (licencia GPL-2.0).

Qué cambia respecto del original:

- El nombre, los íconos y el asistente dicen **Informac Nube**.
- El servidor queda fijo en `https://nube.informac.net`: el usuario solo ingresa su correo y contraseña.
- Los identificadores de Windows son propios, para que pueda convivir con el Nextcloud original.

## Cómo se compila

Todo se hace en GitHub (pestaña **Actions**), sin instalar nada:

1. **Actions → "Compilar Informac Nube (Windows)" → Run workflow.**
2. Tarda alrededor de 1 a 2 horas. Al terminar, el instalador queda en **Releases**.
3. Cada lunes se revisa sola si Nextcloud publicó una versión nueva y, si la hay, la compila.

## Archivos

- `branding/aplicar_marca.py`: aplica nombre, servidor, colores, íconos e identificadores.
- `branding/icon.*` y `branding/logo.*`: ícono y logo de Informac.
- `.github/workflows/compilar-windows.yml`: la receta de compilación.

## Pendiente

- Firma digital del instalador (certificado de firma de código) para evitar el aviso de Windows SmartScreen.
- Ícono: engranaje rojo en vectores (branding/icon.svg), también usado en el instalador (informacnube.ico).
