from resources.tools import *
from resources.tools_settings import *

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys
import time
import os
import subprocess
import json
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
import shutil


####### MAIN #########



# Debug
debug ("JM ADDON INICIO")

# Favoritos

ruta_favoritos = xbmcvfs.translatePath("special://home/userdata/favourites.xml")
ruta_backup = xbmcvfs.translatePath("special://home/userdata/favourites.xml.backup")
ruta_favoritos_JM = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/favourites.xml")


debug("JM favoritos: " + ruta_favoritos)

if xbmcvfs.exists(ruta_favoritos):                            # Verifica si existe la ruta de origen
    debug("JM Se encontró el archivo favoritos")

else:
    debug ("JM No se encontró el archivo favoritos")
    with open(ruta_favoritos, 'w') as file:
        file.write("")  # Crear un archivo vacío
    shutil.copyfile(ruta_favoritos_JM, ruta_favoritos) # Copiar y sobrescribir el archivo origen al archivo destino
    debug ("JM Copiado favoritos de JM")
 
  


#Settings buttons de AJUSTES

debug("JM  sys.argv 0 >> " + str(sys.argv[0]))
debug("JM  sys.argv 1 >> " + str(sys.argv[1]))
debug("JM  sys.argv 2 >> " + str(sys.argv[2]))
debug("JM  sys.argv 3 >> " + str(sys.argv[3]))


if str(sys.argv[2]) == '?parar_acestream_2':
    parar_setting_acestream()

if str(sys.argv[2]) == '?limpiar_cache_setting':
    limpiar_cache_setting()
    
if str(sys.argv[2]) == '?actualizar_links':
    actualizar_links_setting()
    
if str(sys.argv[2]) == '?todos_links_setting':
    todos_links_setting()

if str(sys.argv[2]) == '?actualizar_favoritos_setting':
    actualizar_favoritos_setting()
       
if str(sys.argv[2]) == '?sobreescribir_favoritos_setting':
    sobreescribir_favoritos_setting()

if str(sys.argv[2]) == '?links_manuales_setting':
    links_manuales_setting()


# Indentificar Sistema

debug("JM  Sistema es " + sistema())


#########

def build_url(query):

    return base_url + '?' + urllib.parse.urlencode(query)   #  {"name":"DAZN LaLiga MultiAudio", "link":"df98650743f24a245c44cdf2851e57078f4c487a"}
                                                            #  jm = urllib.parse.urlencode(y) # name=Laliga+multiaudio&link=167e3b44a520cd76d4372f6d30fe6d7ccd524175

####### MENUS CANALES ########

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urllib.parse.parse_qs(sys.argv[2][1:])


### click name
name = args.get('name', None)


### MENU canales

if name is None:

    xbmcplugin.setContent(addon_handle, 'movies')
    listing = []
    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    input_file = open(ruta_ids, mode='r')

    for line in input_file:
        y = json.loads(line)         #  {"name":"DAZN LaLiga MultiAudio", "link":"df98650743f24a245c44cdf2851e57078f4c487a"}
        url = build_url(y)            
        titulo = (y["name"])                            
        list_item = xbmcgui.ListItem(titulo)
        info = list_item.getVideoInfoTag()
        info.setTitle(titulo)
        ####
        if  "DAZN F1" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/F1_logo_v2.png")
           list_item.setArt({'thumb': thumb})
        
        if  "Bar" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/LaligaTvBar.png")
           list_item.setArt({'thumb': thumb})
           
        if  "DAZN LaLiga" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Dazn_liga_logo_v2.png")
           list_item.setArt({'thumb': thumb})     
        
        if  "M. LaLiga" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Mov_liga_logo_v2.png")
           list_item.setArt({'thumb': thumb})
           
        if  "Campeones" in titulo:                                                       
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Campeones_logo_v2.png")
           list_item.setArt({'thumb': thumb})

        if  "Deportes" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Deportes_logo_v2.png")
           list_item.setArt({'thumb': thumb})
           
        if  "DAZN 1" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Motogp_logo_v2.png")
           list_item.setArt({'thumb': thumb})

        if  "DAZN 2" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Dazn_2_logo_v2.png")
           list_item.setArt({'thumb': thumb})

        if  "DAZN 3" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Dazn_3_logo_v2.png")
           list_item.setArt({'thumb': thumb})
  
        if  "M. Golf" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Golf_logo_v2.png")
           list_item.setArt({'thumb': thumb})
         
        if  "EuroSport 1" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Eurosport_1_logo_v2.png")
           list_item.setArt({'thumb': thumb})
                     
        if  "EuroSport 2" in titulo:
           thumb= xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/logos/Eurosport_2_logo_v2.png")
           list_item.setArt({'thumb': thumb})
                          
        
        ####
        list_item.setInfo('video', info)
        list_item.setProperty('IsPlayable', 'false')  
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)

    input_file.close()

### click canal

else:

    nombre = name[0]
    notificacion(nombre)
 
    link = args.get('link', None)
    url = link[0]

    ### Android API

    if sistema() == "android":  
        debug("JM  sistema android canal")
        notificacion("Sistema Android")
        AndroidActivity = 'StartAndroidActivity("","org.acestream.action.start_content","","acestream:?content_id=%s")' % url  ## %s por url
        debug("JM  Abriendo Android")
        xbmc.executebuiltin(AndroidActivity)
    
    ### Linux
    
    else:
        debug("JM Inicio Canal " + nombre + ": "+ url)
        canal(url,nombre)
        debug ("JM Final Canal")
    
    ###

#notificacion("Final")
debug ("JM ADDON FINAL")                                                                            

                                                
