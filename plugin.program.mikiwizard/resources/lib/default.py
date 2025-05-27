import xbmc
import xbmcgui
import xbmcaddon
import os
import shutil
import zipfile
import urllib.request
import datetime

addon = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()

# URL directa del build
build_url = build_url = 
https://github.com/mikicuenta/wizardmiki/tree/main/plugin.program.mikiwizard

# Paths
home_path = xbmc.translatePath("special://home/")
zip_path = os.path.join(home_path, "build.zip")
addons_path = os.path.join(home_path, "addons")
userdata_path = os.path.join(home_path, "userdata")
cache_path = os.path.join(userdata_path, "Cache")
backup_dir = os.path.join(home_path, "backups")

# Crear carpeta de backups si no existe
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Función para limpiar caché
def limpiar_cache():
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path, ignore_errors=True)
        dialog.ok("Miki Wizard", "Caché limpiada correctamente.")
    else:
        dialog.ok("Miki Wizard", "No se encontró caché para limpiar.")

# Función para hacer backup
def hacer_backup():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"backup_{now}.zip")
    dialog.notification("Miki Wizard", "Creando backup...", xbmcgui.NOTIFICATION_INFO, 3000)
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for folder in [addons_path, userdata_path]:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, home_path)
                    backup_zip.write(full_path, arcname)
    dialog.ok("Miki Wizard", "Backup creado correctamente en: " + backup_file)

# Función para instalar build
def instalar_build():
    if dialog.yesno("Miki Wizard", "Este proceso borrará tu configuración actual de Kodi y aplicará tu build personalizada. ¿Deseas continuar?"):
        try:
            hacer_backup()
            limpiar_cache()
            dialog.notification("Miki Wizard", "Descargando build...", xbmcgui.NOTIFICATION_INFO, 3000)
            urllib.request.urlretrieve(build_url, zip_path)
            shutil.rmtree(addons_path, ignore_errors=True)
            shutil.rmtree(userdata_path, ignore_errors=True)
            dialog.notification("Miki Wizard", "Instalando build...", xbmcgui.NOTIFICATION_INFO, 3000)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(home_path)
            os.remove(zip_path)
            dialog.ok("Miki Wizard", "Build instalado correctamente. Kodi se cerrará ahora.")
            xbmc.executebuiltin('Quit()')
        except Exception as e:
            dialog.ok("Error", f"Ocurrió un error: {str(e)}")

# Mostrar menú
opciones = ["Instalar build", "Hacer backup", "Limpiar caché", "Salir"]
seleccion = dialog.select("Miki Wizard - Menú", opciones)

if seleccion == 0:
    instalar_build()
elif seleccion == 1:
    hacer_backup()
elif seleccion == 2:
    limpiar_cache()
else:
    dialog.notification("Miki Wizard", "Operación cancelada.", xbmcgui.NOTIFICATION_INFO, 3000)
