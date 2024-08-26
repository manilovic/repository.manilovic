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
    
    notificacion("Tarda unos segundos....")
    debug ("JM  Tarda unos segundos....")

    notificacion("Espera mensaje de confirmación....")
    debug ("JM  Espera mensaje de confirmación....")
 
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

    href_values = re.findall(r'href="([^"]+)"', busqueda)     # Expresión regular para buscar todos los valores dentro de los atributos href
    result = []                                               # Definir la lista de resultados aquí

    for href in href_values:
       parsed_url = urllib.parse.urlparse(href)                              # Parseamos la URL
       destination_url = urllib.parse.parse_qs(parsed_url.query).get('q')    # Obtener el valor del parámetro 'q' que contiene la URL de destino
    
       if destination_url:                                                   #  se utiliza para verificar si destination_url tiene algún valor antes de intentar acceder al primer elemento de la lista 
         destination_url = destination_url[0]                                # Acceder al primer elemento de la lista
         parsed_destination_url = urllib.parse.urlparse(destination_url)
         name = os.path.basename(parsed_destination_url.path)    	     # Obtener el nombre del archivo de la URL analizada
         name = replace_opcion(name) 
         try:
            response = urllib.request.urlopen(destination_url)
            html_content = response.read().decode('utf-8')
         except urllib.error.URLError as e:
            error_message = str(e)                                           # Convertimos el error en una cadena para almacenarlo
            ##print("Mensaje de error:", error_message)                      # Imprimimos el mensaje de error capturado
            x = "acestream://"
            start = error_message.find(x)
            start = start +12
            end = start + 40
            ace_link = error_message[start:end]
            html_content = None
            items = {"name": name, "link": ace_link}
            result.append(items)                                             # Agregar el diccionario a la lista de resultados
            
            
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
    
    notificacion("Tarda unos segundos....")
    debug ("JM  Tarda unos segundos....")

    notificacion("Espera mensaje de confirmación....")
    debug ("JM  Espera mensaje de confirmación....")
 
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
    
    result = []                                               # Definir la lista de resultados aquí


    for x in canales:
        href_values = re.findall(r'href="([^"]*{}[^"]*)"'.format(x), busqueda)  # Expresión regular para buscar todos los valores dentro de los atributos href que contienen el valor de la variable "canales"
        
        for href in href_values:
           parsed_url = urllib.parse.urlparse(href)                                  # Parseamos la URL
           destination_url = urllib.parse.parse_qs(parsed_url.query).get('q')        # Obtener el valor del parámetro 'q' que contiene la URL de destino
    
           if destination_url:                                                    #  se utiliza para verificar si destination_url tiene algún valor antes de intentar acceder al primer elemento de la lista 
              destination_url = destination_url[0]  # Acceder al primer elemento de la lista
              parsed_destination_url = urllib.parse.urlparse(destination_url)
              name = os.path.basename(parsed_destination_url.path)    		# Obtener el nombre del archivo de la URL analizada
              name = replace_opcion(name) 
              try:
                response = urllib.request.urlopen(destination_url)
                html_content = response.read().decode('utf-8')
              except urllib.error.URLError as e:
                error_message = str(e)                                                               # Convertimos el error en una cadena para almacenarlo
                ##print("Mensaje de error:", error_message)                                    # Imprimimos el mensaje de error capturado
                x = "acestream://"
                start = error_message.find(x)
                start = start +12
                end = start + 40
                ace_link = error_message[start:end]
                html_content = None
                items = {"name": name, "link": ace_link}
                result.append(items)  # Agregar el diccionario a la lista de resultados
        
    result_sorted = sorted(result, key=lambda x: x['name'])
    
    for item in result_sorted:    # Imprimir los elementos ordenados
       json_data = json.dumps(item)                                           # Convertir el diccionario a formato JSON
       file_ids.write(json_data + "\n")                                       # Escribir en el archivo en formato JSON
        
    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")
    
      
    
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
