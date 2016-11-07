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
import sys

#import bs4
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui

#import subtitleSiteLibrary

from subtitleUtils import log, notify

__addon__       = xbmcaddon.Addon()
__version__     = __addon__.getAddonInfo('version')  # Module version
__scriptname__  = __addon__.getAddonInfo('name')
__language__    = __addon__.getLocalizedString
__profile__     = unicode(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'utf-8')
__temp__        = unicode(xbmc.translatePath(os.path.join(__profile__, 'temp', '')), 'utf-8')
__icon__        = __addon__.getAddonInfo('icon')

### get addon info
ADDON        = xbmcaddon.Addon('service.xbmc.versioncheck')
ADDONVERSION = ADDON.getAddonInfo('version')
ADDONNAME    = ADDON.getAddonInfo('name')
ADDONPATH    = ADDON.getAddonInfo('path').decode('utf-8')
ADDONPROFILE = xbmc.translatePath( ADDON.getAddonInfo('profile') ).decode('utf-8')
ICON         = ADDON.getAddonInfo('icon')


class superSearchEngine(object):
    def __init__(self):
        log("[script.renegadestv] Scheduling notifications")



class subtitleEngine:
    #baseSite = [ 'torecUrl', 'bsplayerUrl', 'subcenterUrl','opensubUrl', 'ktuvitUrl' ]
    # constants

    def __init__(self):
        self.urlHandler = "http://www.walla.co.il"
        log(__version__,"[%s] subtitleEngine init" % __scriptname__)
        self.baseSite = [ 'torecUrl', 'bsplayerUrl', 'subcenterUrl','opensubtitlesUrl', 'ktuvitUrl' ]
        self.userAttar = {}
        self.siteCheck = {}
        
    def checkLogins(self,notify_success=False):
        if __addon__.getSetting('debug') == 'true': log(__scriptname__,"checkLogins settings attributes " , "DEBUG" )
        
        if __addon__.getSetting("anonymousSearch") == 'true':
            log(__scriptname__,"%s Anonymouse Site Search Engine %s " % (__version__,str(__addon__.getSetting('anonymousSearch'))), "NOTICE" )
            for i in range(len(self.baseSite)):
                if __addon__.getSetting(self.baseSite[i]+'anon') == "true":
                    if __addon__.getSetting('debug') == 'true': log(__scriptname__," %s Anonymouse login"%(self.baseSite[i]+'anon'),"NOTICE")
                    self.siteCheck[self.baseSite[i]] = {'username' : 'Anonymouse' , 'password' : 'Anonymouse' }
            
        elif __addon__.getSetting("globalSearch") == 'true':
            log(__scriptname__,"%s Global Site Search Engine %s " % (__version__,str(__addon__.getSetting('globalSearch'))), "NOTICE" )
            for i in range(len(self.baseSite)):
                self.siteCheck[self.baseSite[i]] = {'username' : __addon__.getSetting("globalUsername") , 'password' : __addon__.getSetting("globalPassword") }

        elif __addon__.getSetting("specificSiteSearch") == 'true':
            log(__scriptname__,"%s Specific Site Search Engine %s  " % (__version__,str(__addon__.getSetting('specificSiteSearch'))), "NOTICE" )
            for i in range(len(self.baseSite)):
                if __addon__.getSetting('debug') == 'true': log(__scriptname__,"[ %s ] site To status : [ %s ] " %(self.baseSite[i],__addon__.getSetting(self.baseSite[i])), "DEBUG" )
                
                if __addon__.getSetting(self.baseSite[i]) == 'true':
                    if __addon__.getSetting('debug') == 'true': log(__scriptname__, "[%s] - user:pass [%s]:[%s] "%(self.baseSite[i], __addon__.getSetting(self.baseSite[i]+'User'),__addon__.getSetting(baseSite[i]+'Pass')), "NOTICE")
                    self.siteCheck[self.baseSite[i]] = {'username' : __addon__.getSetting(self.baseSite[i]+'User') , 'password' : __addon__.getSetting(self.baseSite[i]+'Pass') }
                    log(__scriptname__," %s Specific Site login"%self.baseSite[i],"NOTICE")
            #log(__scriptname__,"site To Check : [ %s ] " % self.siteCheck, "NOTICE" )
            notify(__scriptname__, __language__, 32001)
            #self.openSelfWindowLoginsCheck()
            
        else :
            self.openSelfDialogUnchacked()
        
        log(__scriptname__,"site To Check : [ %s ] " % self.siteCheck, "NOTICE" )
            
                #self.global = { 'globalUser' : __addon__.getSetting("globalUsername") , 'globalPass' :  __addon__.getSetting("globalUsername") }
    def hostSettingsXML(self):
        
        if __addon__.getSetting("anonymousSearch") == 'true':
            for i in range(len(self.baseSite)):
                if __addon__.getSetting(self.baseSite[i]+'anon') == "true":
                    self.siteCheck[self.baseSite[i]] = {'username' : 'Anonymouse' , 'password' : 'Anonymouse' }
            
            return self.siteCheck
        elif __addon__.getSetting("globalSearch") == 'true':
            for i in range(len(self.baseSite)):
                self.siteCheck[self.baseSite[i]] = {'username' : __addon__.getSetting("globalUsername") , 'password' : __addon__.getSetting("globalPassword") }
            
            return self.siteCheck
        elif __addon__.getSetting("specificSiteSearch") == 'true':
            for i in range(len(self.baseSite)):
                if __addon__.getSetting(self.baseSite[i]) == 'true':
                    self.siteCheck[self.baseSite[i]] = {'username' : __addon__.getSetting(self.baseSite[i]+'User') , 'password' : __addon__.getSetting(self.baseSite[i]+'Pass') }
                
            
            return self.siteCheck   
    
    #def checkSelectedSites(self):
    #    if __addon__.getSetting(self.baseSite[i]) == 'true':
    #    if __addon__.getSetting('debug') == 'true': log(__scriptname__, "[%s] - user:pass [%s]:[%s] "%(self.baseSite[i], __addon__.getSetting(self.baseSite[i]+'User'),__addon__.getSetting(baseSite[i]+'Pass')), "NOTICE")
    #        self.siteCheck[self.baseSite[i]] = {'username' : __addon__.getSetting(self.baseSite[i]+'User') , 'password' : __addon__.getSetting(self.baseSite[i]+'Pass') }
    def openSelfDialogUnchacked(self):
        
        results="You have'nt choosed any type of authentcation \n\
                Please choose one of the folling Authontication Mathod \n\
                In the Authontication Sites Tab \n\
                 - Anonymouse Site Search Engine\n\
                 - Global Site Search Engine\n\
                 - Specific Site Search Engine"
        xbmcgui.Dialog().ok(__scriptname__, results)


    def openSelfWindowLoginsCheck(self):
        log(__scriptname__,"site To Check : [ %s ] " % self.siteCheck, "NOTICE" )
        #dialog = xbmcgui.Dialog()
        #line1 = "This is a simple example of OK dialog"
        #line2 = "Showing this message using"
        #line3 = "XBMC python modules"
        #time = 5000
        #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__scriptname__,line1, time, __icon__))
        #xbmcgui.Dialog().ok(__scriptname__, line1, line2, line3)
        #MyClass()
        #WINDOW = xbmcgui.Window(10000).setProperty('MyProperty', 'MyValue')
        #log("windows",xbmcgui.Window(10000).getProperty('MyProperty'),"NOTICE")
        #Viewer()
        #self.WINDOW.setProperty('PlaylistWatched', "str(played)")
        #self.WINDOW.setProperty('PlaylistCount', "str(numitems)")
        #self.WINDOW.setProperty('PlaylistTVShowCount', "str(tvshowscount)")
        #self.WINDOW.setProperty('PlaylistInProgress', "str(inprogress)")
        #dialog.ok('Warning', 'Could not stop DB sync, you should try again.')
        #try:
        #    WINDOW = xbmcgui.Window(10000)
        #    id = WINDOW.getProperty("")
        #    type = WINDOW.getProperty("")
        #    watchedurl = "{server}/mediabrowser/Users/{UserId}/PlayedItems/%s" % id
        #except: pass
        #    WINDOW.clearProperty("")
ACTION_PREVIOUS_MENU = 10


