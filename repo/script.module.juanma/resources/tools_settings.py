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

    notificacion("Actualizando lista completa links....")
    debug ("JM  Actualizando lista completa links....")
    
    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, mode='w')

    url = "https://www.robertofreijo.com/acestream-ids/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    request = urllib.request.Request(url, headers=headers)     # Crear la solicitud con los encabezados
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')

    busqueda = re.finditer("•", html)                         # Buscar todas las posiciones de "•"
     
    result = []

    for match in busqueda:
        start = match.start()                                                  # Posición de inicio de "•"
        end = html.find('">', start)                                          # Buscar el final después de "•"  
        resultado = html[start:end]
        
        x = "•"
        start = resultado.find(x)
        start = start +1
        end =  resultado.find("<br")
        name = resultado[start:end]
        name = name.strip()
        name = name.lstrip('#') 

        x = "acestream://"
        start = resultado.find(x)
        start = start +12
        end = start + 40
        ace_link = resultado[start:end]

        items = {"name": name, "link": ace_link}
        result.append(items)            
    
            
            
    result_sorted = sorted(result, key=lambda x: x['name'])                  # Ordenar la lista resultante por el valor de la clave "name"


    for item in result_sorted:                                               # Imprimir los elementos ordenados
       json_data = json.dumps(item)                                           # Convertir el diccionario a formato JSON
       file_ids.write(json_data + "\n")                                       # Escribir en el archivo en formato JSON
      

      
    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")
    

def actualizar_links_setting():

    notificacion("Actualizando lista pequeña links....")
    debug ("JM  Actualizando lista pequeña links....")
    
    canales = lista_elementos()
    
    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, mode='w')

    url = "https://www.robertofreijo.com/acestream-ids/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    request = urllib.request.Request(url, headers=headers)     # Crear la solicitud con los encabezados
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')

    busqueda = re.finditer("•", html)                         # Buscar todas las posiciones de "•"
 
    result = []

    for match in busqueda:
        start = match.start()                                                  # Posición de inicio de "•"
        end = html.find('">', start)                                          # Buscar el final después de "•"  
        resultado = html[start:end]
        
        x = "•"
        start = resultado.find(x)
        start = start +1
        end =  resultado.find("<br")
        name = resultado[start:end]
        name = name.strip()
        name = name.lstrip('#') 

        x = "acestream://"
        start = resultado.find(x)
        start = start +12
        end = start + 40
        ace_link = resultado[start:end]

        for canal in canales:
            if canal in name:
                items = {"name": name, "link": ace_link}
                result.append(items)


    result_sorted = sorted(result, key=lambda x: x['name'])                  # Ordenar la lista resultante por el valor de la clave "name"
   

    for item in result_sorted:    # Imprimir los elementos ordenados
       json_data = json.dumps(item)                                           # Convertir el diccionario a formato JSON
       file_ids.write(json_data + "\n")                                       # Escribir en el archivo en formato JSON
        
    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")
        
        
def sobreescribir_favoritos_setting():

    ruta_favoritos = xbmcvfs.translatePath("special://home/userdata/favourites.xml")
    ruta_backup = xbmcvfs.translatePath("special://home/userdata/favourites.xml.backup")
    ruta_favoritos_JM = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/favourites.xml")
    ruta_test = xbmcvfs.translatePath("special://home/userdata/favourites.xml.test")
    
    debug ("JM Sobreescribiendo archivo favoritos")
    notificacion(" Sobreescribiendo archivo favoritos")
    
    with open(ruta_favoritos, 'w') as file:
        file.write("")  # Crear un archivo vacío
    shutil.copyfile(ruta_favoritos_JM, ruta_favoritos) # Copiar y sobrescribir el archivo origen al archivo destino
    debug ("JM Copiado favoritos de JM")
    notificacion("Favoritos actualizado")
    notificacion("Reiniciar Kodi para que surtan efecto los cambios")
    debug ("JM Favoritos actualizados")

    
def actualizar_favoritos_setting():

    ruta_favoritos = xbmcvfs.translatePath("special://home/userdata/favourites.xml")
    ruta_backup = xbmcvfs.translatePath("special://home/userdata/favourites.xml.backup")
    ruta_favoritos_JM = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/favourites.xml")
    ruta_test = xbmcvfs.translatePath("special://home/userdata/favourites.xml.test")
    
    if xbmcvfs.exists(ruta_favoritos):                              # Verifica si existe la ruta de origen
        debug ("JM Se encontró archivo Favoritos")
        shutil.copyfile(ruta_favoritos, ruta_backup)                # Copiar y sobrescribir el archivo origen al archivo backup
        with xbmcvfs.File(ruta_backup, 'r') as file_origen:
            lines = file_origen.read().splitlines()                
        with xbmcvfs.File(ruta_test, 'w') as file_destino:
            for line in lines[:-1]:                                 # Slice to skip the last line
                file_destino.write(line + "\n")
        with xbmcvfs.File(ruta_test, 'r') as file_test:
            existing_lines = file_test.read().splitlines()

        
        with xbmcvfs.File(ruta_favoritos_JM, 'r') as file_test:
            lines = file_test.read().splitlines()
        with xbmcvfs.File(ruta_test, 'w') as file_destino:
            for line in lines[1:]:                                  # Slice to skip the first line
                file_destino.write(line + "\n")
        with xbmcvfs.File(ruta_test, 'r') as file_origen:
            lines_to_append = file_origen.read().splitlines()

        combined_lines = existing_lines + lines_to_append
        with xbmcvfs.File(ruta_favoritos, 'w') as file_destino:
            for line in combined_lines:
                file_destino.write(line + "\n")

    notificacion("Favoritos actualizado")
    notificacion("Reiniciar Kodi para que surtan efecto los cambios")
    debug ("JM Favoritos actualizados")
