import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import subprocess
import sys
import time
import os
import platform
import urllib.request
import re
import json
import shutil


from resources.tools import *


def parar_setting_acestream():
    
    if "ANDROID_STORAGE" in os.environ:
        SO = "android"
        exit(0)

    if sistema() == "Ubuntu":
        pkill_acestream = "pkill acestream"
        subprocess.run(pkill_acestream, shell=True)
        debug("JM  Parada Forzosa Acestream UBUNTU")
    elif sistema() == "arm":
        ruta_acestream_stop = xbmcvfs.translatePath("special://home/userdata/addon_data/script.module.horus/acestream.engine/acestream.stop")
        subprocess.run([ "sudo", ruta_acestream_stop ]) 
        debug ("JM  Parada Forzosa Acestream ARM")
    else:
        pass

    time.sleep(2)

    p = subprocess.run('ps -ef | grep aces', shell=True, capture_output=True)    ###'minipc     60569   60567  0 23:07 pts/0    00:00:00 grep aces\n'
    if not b'acestream' in p.stdout:
        notificacion("Motor Acestream cerrado")
        debug("JM  Motor Acestream cerrado")
    else:
        notificacion("Motor Acestream NO cerrado")
        debug("JM  Motor Acestream NO cerrado")

    time.sleep(2)

    return(debug("JM  Motor Acestream parado"))
    

def limpiar_cache_setting():
        
    if "ANDROID_STORAGE" in os.environ:
        pathTV = '/storage/emulated/0/org.acestream.engine/.ACEStream/.acestream_cache/'
        pathPHONE = '/storage/emulated/0/Android/data/org.acestream.media.atv/files/.ACEStream/.acestream_cache/'
        
        ruta_TV = os.path.exists(pathTV)
        ruta_PHONE = os.path.exists(pathPHONE)
                
        if str(ruta_TV) == "True":
            debug("JM  caché TV es "+ str(ruta_TV))     
            notificacion("Limpiando cache")
            shutil.rmtree(pathTV, ignore_errors=True)
            debug("JM  caché borrado")
        elif str(ruta_PHONE) == "True":
            debug("JM  caché TV es "+ str(ruta_PHONE))     
            notificacion("Limpiando cache")
            shutil.rmtree(pathPHONE, ignore_errors=True)
            debug("JM  caché borrado")
            
    elif sistema() == "Ubuntu":
        notificacion("Limpiando caché")
        debug("JM  Limpiando caché")
        comando = "find  /home/*/snap/acestreamplayer/??/.ACEStream/.acestream_cache/* -maxdepth 1 -mmin +120 -delete"
        subprocess.run(comando, shell=True)
        debug("JM  caché borrado")
        
    elif sistema() == "arm": 
        comando = xbmcvfs.translatePath("special://home/userdata/addon_data/script.module.horus/acestream.engine/????????????")
        subprocess.run(comando, shell=True)
        notificacion("Limpiando cache")
        debug("JM  Limpiando caché")    ###############provisional ruta ARM
    else:
        pass
        
    notificacion("Caché limpiado")
    return(debug("JM  Caché limpiado"))


def replace_opcion(name):
    name = name.replace("o1", "Opción 1")
    name = name.replace("o2", "Opción 2")
    name = name.replace("o3", "Opción 3")
    name = name.replace("O 3", "Opción 3")
    name = name.replace("m-","Movistar-")
    name = name.replace("channel","")  
    name = name.replace("deportes","M. Deportes-") 
    name = name.replace("campeones","M. Liga Campeones-") 
    name = name.replace("-", " ")  # Eliminar el guion "-"
    name = " ".join(word.capitalize() for word in name.split())  # Convertir la primera letra de cada palabra en mayúscula
    return name



