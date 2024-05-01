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
import requests

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


def actualizar_links_setting():
    notificacion("Actualizando links acestream...")
    debug("JM  Actualizando links acestream")

    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")  ############################ LINK
    file_ids = open(ruta_ids, mode='w')

    url = "https://sites.google.com/view/elplandeportes/inicio"
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    x = "data-tooltip=\"DAZN LaLiga\""
    start = html.find(x)
    y = "Reddit https://reddit.com/user/No_Land656"
    end = html.find(y)
    busqueda = html[start:end]

    canales = ["dazn", "m-ligatv", "deportes", "campeones", "golf"]

    for x in canales:
        href_values = re.findall(r'href="([^"]*{}[^"]*)"'.format(x), busqueda)  # Expresión regular para buscar todos los valores dentro de los atributos href que contienen el valor de la variable "canales"
        
        for href in href_values:
            parsed_url = urllib.parse.urlparse(href)  # Parseamos la URL
            destination_url = urllib.parse.parse_qs(parsed_url.query).get('q')  # Obtener el valor del parámetro 'q' que contiene la URL de destino
    
            if destination_url:
                destination_url = destination_url[0]  # Obtener el primer elemento de la lista
                parsed_destination_url = urllib.parse.urlparse(destination_url)
                name = os.path.basename(parsed_destination_url.path)
                name = replace_opcion(name)
                try:
                    response = requests.get(destination_url)
                    html_content = response.text
                except requests.exceptions.RequestException as e:
                    error_message = str(e)  # Convertimos el error en una cadena para almacenarlo
                    print("Mensaje de error:", error_message)  # Imprimimos el mensaje de error capturado
                    x = "acestream://"
                    start = error_message.find(x)
                    start = start + 12
                    end = start + 40
                    ace_link = error_message[start:end]
                    html_content = None
                    items = {"name": name, "link": ace_link}
                    json_data = json.dumps(items)  # Convertir el diccionario a formato JSON
                    file_ids.write(json_data + "\n")  # Escribir en el archivo en formato JSON

    file_ids.close()
    notificacion("Links actualizados")
    debug("JM  Links actualizados")

    
def todos_links_setting():

    notificacion("Actualizando lista completa links...")
    debug ("JM  Actualizando lista completa links")
    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, mode='w')    
    
    url = "https://sites.google.com/view/elplandeportes/inicio"
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    x = "data-tooltip=\"DAZN LaLiga\""
    start = html.find(x)
    y = "Reddit https://reddit.com/user/No_Land656"
    end = html.find(y)
    busqueda = html[start:end]

    href_values = re.findall(r'href="([^"]+)"', busqueda)  # Expresión regular para buscar todos los valores dentro de los atributos href
    
    for href in href_values:
        parsed_url = urllib.parse.urlparse(href)  # Parseamos la URL
        destination_url = urllib.parse.parse_qs(parsed_url.query).get('q')  # Obtener el valor del parámetro 'q' que contiene la URL de destino
    
        if destination_url:
            destination_url = destination_url[0]  # Obtener el primer elemento de la lista
            parsed_destination_url = urllib.parse.urlparse(destination_url)
            name = os.path.basename(parsed_destination_url.path)
            name = replace_opcion(name)

        try:
            response = requests.get(destination_url)
            html_content = response.text
        except requests.exceptions.RequestException as e:
            error_message = str(e)  # Convertimos el error en una cadena para almacenarlo
            print("Mensaje de error:", error_message)  # Imprimimos el mensaje de error capturado
            x = "acestream://"
            start = error_message.find(x)
            start = start +12
            end = start + 40
            ace_link = error_message[start:end]
            html_content = None
            items = {"name": name, "link": ace_link}
            json_data = json.dumps(items)  # Convertir el diccionario a formato JSON
            file_ids.write(json_data + "\n")  # Escribir en el archivo en formato JSON
    
    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")
