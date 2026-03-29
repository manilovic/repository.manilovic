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
        

    debug ("JM caché")
    debug ("JM " + str(os.environ))
              
    if "ANDROID_STORAGE" in os.environ:  ########### No hay permisos en ANDROID para borrar
        
        # Ruta que deseas listar
        path = "/storage/emulated/0/Android/data/"
        try:
        # Listar contenido del directorio
            files_and_dirs = os.listdir(path)
            debug("JM " + path)
            
            for item in files_and_dirs:
            	debug("JM lista" + item)
        except FileNotFoundError:
            debug("JM no existe" + path)
        except PermissionError:              
            debug("JM no permisos" + path)   ######## ERROR 
        

        path = '/storage/emulated/0/Android/data/org.acestream.node/files/.ACEStream/.acestream_cache/'  ### ruta correcta
        ruta_PHONE = os.path.exists(path)
        debug("JM ruta_PHONE es " + str(ruta_PHONE))
        debug("JM ruta_PHONE es " + str(path))
        
                                    
        if str(ruta_PHONE) == "True":
            shutil.rmtree(path, ignore_errors=True)
            debug("JM  caché borrado")

            
    elif sistema() == "Ubuntu":
    
        notificacion("Limpiando caché UBUNTU")
        debug("JM  Limpiando caché UBUNTU")
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


def actualizar_links_elastic(palabra=None):

    notificacion("Buscando elastic links....")
    debug ("JM Buscando elastic links....")
    
    if palabra is None:
        palabra = palabra_buscador()
    debug (f"JM Buscando {palabra}")
    notificacion (f'JM Buscando "{palabra}"....')

    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, encoding="utf-8", mode='w')

    if palabra == "ext":
        url = "http://manilovic.ddns.net:6704/acestreams/_search"
        payload = {"size": 9000,"query": {"bool": {"must": [{"term": {"foreign": True}}]}}}
    else:
        url = "http://manilovic.ddns.net:6704/acestreams/_search"
        payload = {"size": 1000,"query": {"match_phrase": {"name": palabra }}}

    req = urllib.request.Request(url,data=json.dumps(payload).encode("utf-8"),headers={"Content-Type": "application/json"},method="POST")

    with urllib.request.urlopen(req) as response:
        result_json = json.loads(response.read().decode("utf-8"))

        hits = result_json.get("hits", {}).get("hits", [])

        for hit in hits:
            source = hit.get("_source", {})

            log_enabled = getsetting("canales_on").strip().lower()  # elimina espacios y pasa a minúscula
            debug(f"JM setting {log_enabled}")

            if log_enabled == "true":
                if source.get("running") is False:
                    continue

                    
            debug(f"JM guardando {source}")
            json.dump(source, file_ids, ensure_ascii=False)
            file_ids.write("\n")
         
    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")


def sobrescribir_favoritos():

    ruta_addon = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/favourites.xml")
    ruta_usuario = xbmcvfs.translatePath("special://userdata/favourites.xml")

    try:
        # Verificar que el archivo del addon exista
        if not xbmcvfs.exists(ruta_addon):
            print(f"[ERROR] No se encontró el favourites.xml en el addon: {ruta_addon}")
            return False

        # Copiar y sobrescribir
        shutil.copyfile(ruta_addon, ruta_usuario)
        print(f"[INFO] Favoritos sobrescritos correctamente: {ruta_usuario}")
        return True

    except Exception as e:
        print(f"[ERROR] Falló al sobrescribir favoritos: {e}")
        return False
