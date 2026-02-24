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


def todos_links_setting():

    notificacion("Actualizando lista manual completa links....")
    debug ("JM  Actualizando lista manual completa links....")
    
    result = []
    
    ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    idsmanuales = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids/manualesids.json")
    
    with open(idsmanuales, encoding="utf-8", mode="r") as file:
       lines = file.readlines()
    
    for line in lines:
       data = json.loads(line)
       result.append(data)
       debug (f"JM canales {data}")
                
    
    result_sorted = sorted(result, key=lambda x: x['name'])                  # Ordenar la lista resultante por el valor de la clave "name"
    
    
    with open(ids, encoding="utf-8", mode='w') as file_ids:
       for item in result:                                                # Imprimir los elementos ordenados
          json_data = json.dumps(item)# Convertir el diccionario a formato JSON
          print(json_data)
          file_ids.write(json_data + "\n")                                       # Escribir en el archivo en formato JSON
        
    
   
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")
      



def todos_malos_setting():

    notificacion("Actualizando lista mala....")
    debug ("JM  Actualizando lista mala....")
    
    result = []
    
    ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    idsmanuales = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids/malos_ids.json")
    
    with open(idsmanuales, encoding="utf-8", mode="r") as file:
       lines = file.readlines()
    
    for line in lines:
       data = json.loads(line)
       result.append(data)
       debug (f"JM canales {data}")
                
    
    result_sorted = sorted(result, key=lambda x: x['name'])                  # Ordenar la lista resultante por el valor de la clave "name" 

    with open(ids, encoding="utf-8", mode='w') as file_ids:
       for item in result:                                                # Imprimir los elementos ordenados
          json_data = json.dumps(item)                                            # Convertir el diccionario a formato JSON
          file_ids.write(json_data + "\n")                                       # Escribir en el archivo en formato JSON
        
    
   
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")


def actualizar_links_acesearch():

    notificacion("Buscando acestreamsearch links....")
    debug ("JM Buscando acestreamsearch links....")
    
    
    teclado = xbmcgui.Dialog()
    palabra = teclado.input("¿Qué canal quieres buscar en acestream search?", type=xbmcgui.INPUT_ALPHANUM)
      
    if not palabra:
       palabra = "sports"  # Valor por defecto

    
    #palabra= palabra_buscador()
    debug (f"JM Buscando {palabra}")
    notificacion (f'JM Buscando "{palabra}"....')

  
    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, encoding="utf-8", mode='w')


    url = f"http://192.168.1.48:5000/buscar?q={palabra}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    request = urllib.request.Request(url, headers=headers)     # Crear la solicitud con los encabezados
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    
    debug (f"JM canales {html}")
    
    data = json.loads(html)  # Decodificar el JSON
    debug (f"JM loads {data}")
    
    for item in data:
       debug (f"JM canales {item}")
       
       # Convertir el diccionario en un string JSON y escribirlo en el archivo
       json_data = json.dumps(item, ensure_ascii=False)
       file_ids.write(json_data + "\n")     

    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")


def links_manuales_setting():

    notificacion("Actualizando lista manual...")
    debug("JM  Actualizando lista manual...")

    canales = lista_elementos()
    debug(f"JM canales {canales}")

    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")

    with open(ruta_ids, mode="w", encoding="utf-8") as file_ids:     

        for canal in canales:
            debug(f"JM buscando {canal}")

            if canal == "Extranjeras":
                url = "http://manilovic.ddns.net:9200/acestreams/_search"
                payload = {"size": 9000,"query": {"bool": {"must": [{"term": {"valido": True}}]}}}
            else:        
                url = "http://manilovic.ddns.net:9200/acestreams/_search"
                payload = {"size": 1000,"query": {"match_phrase": {"name": canal }}}

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

                    #if log_enabled == "true" and not source.get("running", True):  #### al reves????????????????
                    #    continue  # saltar los que no estén en running
                    
                    debug(f"JM guardando {source}")

                    json.dump(source, file_ids, ensure_ascii=False)
                    file_ids.write("\n")

    file_ids.close()
    notificacion("Links actualizados")
    debug("JM  Links actualizados")
