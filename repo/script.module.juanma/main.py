# -*- coding: utf-8 -*-

from resources.tools import *
from resources.tools_settings import *

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import sys
import os
import json
import time
import shutil
import urllib.request
import urllib.parse
from urllib.parse import parse_qsl




def guardar_historial_busqueda(palabra):

    ruta = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/historial_busquedas.json")

    historial = []

    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            historial = json.load(f)

    if palabra not in historial:
        historial.insert(0, palabra)

    historial = historial[:10]

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False)


def buscar():

    keyboard = xbmc.Keyboard('', 'Buscar canal, ext (extranjeras)')
    keyboard.doModal()

    if not keyboard.isConfirmed():
        return

    palabra = keyboard.getText()

    if not palabra:
        return

    guardar_historial_busqueda(palabra)

    actualizar_links_elastic(palabra)


def mostrar_historial():

    ruta = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/historial_busquedas.json")

    if not os.path.exists(ruta):
        xbmcgui.Dialog().notification("JM", "Sin historial")
        return

    listing = []

    with open(ruta, encoding="utf-8") as f:
        historial = json.load(f)

    for palabra in historial:

        url = build_url({
            'action': 'buscar_historial',
            'palabra': palabra
        })

        li = xbmcgui.ListItem("🔎 " + palabra)
        listing.append((url, li, True))

    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)




####### MAIN #########

debug("JM ADDON INICIO")


# Indentificar Sistema
debug("JM  Sistema es " + sistema())


debug("JM  sys.argv 0 >> " + str(sys.argv[0]))
debug("JM  sys.argv 1 >> " + str(sys.argv[1]))
debug("JM  sys.argv 2 >> " + str(sys.argv[2]))
debug("JM  sys.argv 3 >> " + str(sys.argv[3]))


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))

# ==========================================================
# ACCIONES DESDE SETTINGS
# ==========================================================

if str(sys.argv[2]) == '?parar_acestream_2':
    parar_setting_acestream()

elif str(sys.argv[2]) == '?limpiar_cache_setting':
    limpiar_cache_setting()


# ==========================================================
# ENTRADA NORMAL AL ADDON (SIN ACCIÓN)
# ==========================================================

if not sys.argv[2]:

    # --- Favoritos (solo en entrada normal) ---
    ruta_favoritos = xbmcvfs.translatePath("special://home/userdata/favourites.xml")
    ruta_favoritos_JM = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/favourites.xml")

    try:
        shutil.copyfile(ruta_favoritos_JM, ruta_favoritos)
        debug("JM Copiado favoritos de JM")
    except Exception as e:
        debug("JM Error copiando favoritos: " + str(e))


# ==========================================================
# CONSTRUCCIÓN MENÚ
# ==========================================================

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)


args = urllib.parse.parse_qs(sys.argv[2][1:])
action = args.get('action', None)






### click name

name = args.get('name', None) 



if action == ['buscar']:
    buscar()

elif action == ['historial']:
    mostrar_historial()

elif action == ['buscar_historial']:

    palabra = args.get("palabra")[0]
    actualizar_links_elastic(palabra)


# ==========================================================
# LISTADO PRINCIPAL ### menu canales
# ==========================================================

if name is None:

    xbmcplugin.setContent(addon_handle, 'movies')
    listing = []

    # BUSCADOR
    url = build_url({'action': 'buscar'})
    li = xbmcgui.ListItem("🔎 Buscar canal")
    listing.append((url, li, True))

    # HISTORIAL
    url = build_url({'action': 'historial'})
    li = xbmcgui.ListItem("🕘 Historial búsquedas")
    listing.append((url, li, True))

    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")

    if not os.path.exists(ruta_ids):
        debug("JM ids.json no existe")
        xbmcplugin.endOfDirectory(addon_handle)
        sys.exit()

    with open(ruta_ids, encoding="utf-8", mode='r') as input_file:

        for line in input_file:

            y = json.loads(line)  # {"name":"DAZN LaLiga MultiAudio", "link":"df98650743f24a245c44cdf2851e57078f4c487a"}

            url = build_url(y)
            titulo = y["name"]

            # Color por running
            estado = y.get("running")

            # ===== Colores según running =====
            estado = y.get("running")
            if str(estado).lower() == "true":
                titulo = f"[COLOR lime]{titulo}[/COLOR]"
            elif str(estado).lower() == "false":
                titulo = f"[COLOR red]{titulo}[/COLOR]"

            # ===== Crear ListItem =====
            list_item = xbmcgui.ListItem(titulo)
            info = list_item.getVideoInfoTag()
            info.setTitle(titulo)

            list_item.setInfo('video', info)
            list_item.setProperty('IsPlayable', 'false')

            listing.append((url, list_item, False))

    # ===== Añadir todos los items y terminar directorio =====  
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)


# ==========================================================
# CLICK EN CANAL
# ==========================================================

else:

    nombre = name[0]
    notificacion(nombre)

    link = args.get('link', None)
    url = link[0]
    
    if sistema() == "android":  
        debug("JM  sistema Android canal")
        notificacion("Sistema Android")
        AndroidActivity = 'StartAndroidActivity("","org.acestream.action.start_content","","acestream:?content_id=%s")' % url  ## %s por url
        debug("JM  Abriendo Android")
        xbmc.executebuiltin(AndroidActivity)
    
    ### Linux
    
    else:
        notificacion("JM  Sistema es " + sistema())
        debug("JM  Sistema es " + sistema())
        debug("JM Inicio Canal " + nombre + ": "+ url)
        canal(url,nombre)
        debug ("JM Final Canal")

debug("JM ADDON FINAL")

