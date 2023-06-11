from resources.tools import *
import urllib.request
import re
import json



# Debug
debug ("JM ADDON MANILINKS INICIO")


notificacion("Actualizando links acestream")
debug ("JM  Actualizando links acestream")

ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
file_ids = open(ruta_ids, mode='w')


response = urllib.request.urlopen("https://hackmd.io/@DEPORTES/AP-ID")
html = response.read().decode('utf-8')

canales = ["DAZN LaLiga 1080p","DAZN LaLiga 2","M. LaLiga 1080p","M. LaLiga 2 ","M.L. Campeones 1080p","M.L. Campeones 2","M. Deportes 1080p","DAZN 1", "DAZN 2","DAZN F1 1080p","M. Golf 1080p"]


for x in canales:
  
  start = html.find(x)
  end =  start + 300
  busqueda = html[start:end]
  busqueda = busqueda.split('\n', 1)[0]
  
  while "acestream" in busqueda:
    start = busqueda.find("acestream://")
    end = start + 52
    ace_link = busqueda[start:end]              ## acestream://60cf60019aeef9af6.... ##
    busqueda = busqueda.replace(ace_link, " ")  ## borramos para siguiente iteraccion ##
    
    ace_link = ace_link.replace("acestream://","") 
    items ={"name":x, "link":ace_link}
    y = json.dumps(items)
    #print(y)
    
    
    file_ids.write(y)
    file_ids.write("\n")
    
    
    
file_ids.close()

notificacion("Links actualizados")
 
    
# Debug                 
debug ("JM  ADDON MANILINKS FINAL")

# Salir
exit(0)
