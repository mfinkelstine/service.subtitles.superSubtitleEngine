# -*- coding: utf-8 -*-

import HTMLParser
import os
import re
import urllib
import urllib2
import unicodedata
import json
import zlib
import shutil
#import bs4
import xbmc
import xbmcvfs
import xbmcaddon


from subtitleUtils import log, notify

__addon__       = xbmcaddon.Addon()
__version__     = __addon__.getAddonInfo('version')  # Module version
__scriptname__  = __addon__.getAddonInfo('name')
__language__    = __addon__.getLocalizedString
__profile__     = unicode(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'utf-8')
__temp__        = unicode(xbmc.translatePath(os.path.join(__profile__, 'temp', '')), 'utf-8')


class superSearchEngine(object):
    def __init__(self):
        log("[script.renegadestv] Scheduling notifications")



class subtitleEngine:
    baseSite = [ 'torecUrl', 'bsplayerUrl', 'subcenterUrl','opensubUrl', 'ktuvitUrl' ]
    
    def __init__(self):
        self.urlHandler = "http://www.walla.co.il"
        log(__version__,"[%s] subtitleEngine init" % __scriptname__)
        self.userAttar = {}
        
    def checkLogins(self,notify_success=False):
        #email       = __addon__.getSetting("Email")
        #password    = __addon__.getSetting("Password")
        log(__scriptname__,"%s addon settings attributes " % __addon__, "NOTICE" )

        if __addon__.getSetting("anonymousSearch") == 'true':
            log(__scriptname__,"%s attr anonymousSearch %s " % (__version__,str(__addon__.getSetting('anonymousSearch'))), "NOTICE" )
            #self.useranon 
            #self.passanon
        elif __addon__.getSetting("specificSiteSearch") == 'true':
            log(__scriptname__,"%s attr specificSiteSearch %s  " % (__version__,str(__addon__.getSetting('specificSiteSearch'))), "NOTICE" )
            for i in len(baseSite):
                log(__scriptname__,"%s attr globalSearch %s " % baseSite[i], "NOTICE" )
                
        elif __addon__.getSetting("globalSearch") == 'true':    
            log(__scriptname__,"%s attr globalSearch %s " % (__version__,str(__addon__.getSetting('globalSearch'))), "NOTICE" )
            log(__scriptname__,"global user [%s] pass [%s] "%(__addon__.getSetting("globalUsername") , __addon__.getSetting("globalPassword")), "NOTICE")
                #self.global = { 'globalUser' : __addon__.getSetting("globalUsername") , 'globalPass' :  __addon__.getSetting("globalUsername") }


                