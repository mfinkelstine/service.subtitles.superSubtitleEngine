import sys
import struct
import urllib2
import urlparse
import cookielib
from os import path
from httplib import HTTPConnection

import xbmcaddon
import xbmc
import xbmcgui



__addon__       = xbmcaddon.Addon()
__version__     = __addon__.getAddonInfo('version')  # Module version
__scriptname__  = __addon__.getAddonInfo('name')
__language__    = __addon__.getLocalizedString
__profile__     = unicode(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'utf-8')
__temp__        = unicode(xbmc.translatePath(path.join(__profile__, 'temp', '')), 'utf-8')


def log(module, msg, level=None):
    #logLevel="xbmc.%s"%level
    #LOGDEBUG  = 0, LOGINFO = 1,LOGNOTICE = 2,LOGWARNING = 3,LOGERROR = 4
    #LOGSEVERE = 5, LOGFATAL = 6, LOGNONE = 7 
    if level == "DEBUG":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGDEBUG)
    elif level == "INFO":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGINFO)
    elif level == "NOTICE":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGNOTICE)
    elif level == "WARNING":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGWARNING)
    elif level == "ERROR":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGERROR)
    elif level == "SEVERE":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGSEVERE)
    elif level == "FATAL":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGFATAL)
    elif level == "NONE":
        xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGNONE)

def logv(module, msg):
    xbmc.log((u"### [%s] - %s" % (module, msg)).encode('utf-8'), level=xbmc.LOGSEVERE )

def notify(script_name, language, string_id):
    xbmc.executebuiltin((u'Notification(%s,%s)' % (script_name, language(string_id))).encode('utf-8'))

def get_params(params_str=""):
    params_str = params_str or sys.argv[2]
    return dict(urlparse.parse_qsl(params_str.lstrip('?')))
