import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs


def debug(message):

    log_enabled = getsetting("debug")
    if log_enabled == "true":
        xbmc.log(message, xbmc.LOGINFO)


def getsetting(settingname):

    setting = xbmcaddon.Addon().getSetting(settingname)
    return setting


def notificacion(line1):

    __addon__ = xbmcaddon.Addon()
    __addonname__ = __addon__.getAddonInfo('name')
    __icon__ = __addon__.getAddonInfo('icon')
    #line1 = "No Server"
    timeml = 5000 #in miliseconds
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeml, __icon__))
