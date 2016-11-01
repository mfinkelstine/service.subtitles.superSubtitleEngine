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
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self):
        self.urlHandler = "http://www.walla.co.il"
        log(__version__,"[%s] subtitleEngine init" % __scriptname__)
#        self.WINDOW = xbmcgui.Window(10000)
        self.baseSite = [ 'torecUrl', 'bsplayerUrl', 'subcenterUrl','opensubUrl', 'ktuvitUrl' ]
        self.userAttar = {}
        self.siteCheck = {}
        
    def checkLogins(self,notify_success=False):
        #baseSite = [ 'torecUrl', 'bsplayerUrl', 'subcenterUrl','opensubtitlesUrl', 'ktuvitUrl' ]
        log(__scriptname__,"checkLogins settings attributes " , "NOTICE" )
        
        if __addon__.getSetting("anonymousSearch") == 'true':
            log(__scriptname__,"%s Anonymouse Site Search Engine %s " % (__version__,str(__addon__.getSetting('anonymousSearch'))), "NOTICE" )
            for i in range(len(self.baseSite)):
                if __addon__.getSetting(self.baseSite[i]+'anon') == "true":
                    log(__scriptname__," %s Anonymouse Site login"%(self.baseSite[i]+'anon'),"NOTICE")
            
            #if __addon__.getSetting(self.baseSite[i]+'anon') == 'true':
            #    log(__scriptname__,"%s attr anonymousSearch %s " % (__version__,str(self.baseSite[i]), "NOTICE" )
            #for i in range(len(self.baseSite)):
                #if __addon__.getSetting(self.baseSite[i]) == 'true':
            #    log(__scriptname__,"%s attr anonymousSearch %s " % (__version__,str(self.baseSite[i]), "NOTICE" )
        elif __addon__.getSetting("globalSearch") == 'true':    
            log(__scriptname__,"%s Global Site Search Engine %s " % (__version__,str(__addon__.getSetting('globalSearch'))), "NOTICE" )
            log(__scriptname__,"global user [%s] pass [%s] "%(__addon__.getSetting("globalUsername") , __addon__.getSetting("globalPassword")), "NOTICE")
            log(__scriptname__," %s Global Site login"%self.baseSite[i],"NOTICE")

        elif __addon__.getSetting("specificSiteSearch") == 'true':
            log(__scriptname__,"%s Specific Site Search Engine %s  " % (__version__,str(__addon__.getSetting('specificSiteSearch'))), "NOTICE" )
            for i in range(len(self.baseSite)):
                if __addon__.getSetting('debug') == 'true': log(__scriptname__,"[ %s ] site To status : [ %s ] " %(self.baseSite[i],__addon__.getSetting(self.baseSite[i])), "DEBUG" )
                
                if __addon__.getSetting(self.baseSite[i]) == 'true':
                    if __addon__.getSetting('debug') == 'true': log(__scriptname__, "[%s] - user:pass [%s]:[%s] "%(self.baseSite[i], __addon__.getSetting(self.baseSite[i]+'User'),__addon__.getSetting(baseSite[i]+'Pass')), "NOTICE")
                    self.siteCheck[self.baseSite[i]] = {'username' : __addon__.getSetting(self.baseSite[i]+'User') , 'password' : __addon__.getSetting(self.baseSite[i]+'Pass') }
                    log(__scriptname__," %s Specific Site login"%self.baseSite[i],"NOTICE")
            log(__scriptname__,"site To Check : [ %s ] " % self.siteCheck, "NOTICE" )
            notify(__scriptname__, __language__, 32001)
            #self.openSelfWindowLoginsCheck()
            
        else :
            self.openSelfDialogUnchacked()
            
                #self.global = { 'globalUser' : __addon__.getSetting("globalUsername") , 'globalPass' :  __addon__.getSetting("globalUsername") }
    def hostsLoginCheck(self):
        print "host"
    
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

class MyClass(xbmcgui.WindowDialog):
    def __init__(self):
        #background = xbmcgui.ControlImage(40, 40, 270, 154, 'ContentPanel.png')
        #self.addControl(background)
        self.strActionInfo = xbmcgui.ControlLabel(150, 400, 200, 200, '', 'font13', '0xFFFF00FF')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel('')
        self.button0 = xbmcgui.ControlButton(42, 42, 270, 30, "shortName1")
        self.addControl(self.button0)
        self.button1 = xbmcgui.ControlButton(42, 72, 270, 30, "shortName2")
        self.addControl(self.button1)
        self.button2 = xbmcgui.ControlButton(42, 102, 270, 30, "shortName3")
        self.addControl(self.button2)
        self.button3 = xbmcgui.ControlButton(42, 132, 270, 30, "shortName4")
        self.addControl(self.button3)
        self.button4 = xbmcgui.ControlButton(42, 162, 270, 30, "shortName5")
        self.addControl(self.button4)
        self.setFocus(self.button0)
        self.button0.controlDown(self.button1)
        self.button0.controlUp(self.button4)
        self.button1.controlUp(self.button0)
        self.button1.controlDown(self.button2)
        self.button2.controlUp(self.button1)
        self.button2.controlDown(self.button3)
        self.button3.controlUp(self.button2)
        self.button3.controlDown(self.button4)
        self.button4.controlUp(self.button3)
        self.button4.controlDown(self.button0)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        if control == self.button0:
            self.close()
        if control == self.button1:
            self.close()
        if control == self.button2:
            self.close()
        if control == self.button3:
            self.close()
        if control == self.button4:
            self.close()

#mydisplay = MyClass()
#mydisplay .doModal()
#del mydisplay

class Viewer:
        # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW,))
        # get window
        self.window = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(100)
        # set controls
        self.setControls()

    def setControls(self):
        #get header, text
        heading, text = self.getText()
        # set heading
        self.window.getControl(self.CONTROL_LABEL).setLabel("%s : %s" % (ADDONNAME, heading, ))
        # set text
        self.window.getControl(self.CONTROL_TEXTBOX).setText(text)
        xbmc.sleep(2000)

    def getText(self):
        try:
            if sys.argv[ 1 ] == "gotham-alpha_notice":
                return "Call to Gotham alpha users", self.readFile(os.path.join(ADDONPATH , "resources/gotham-alpha_notice.txt"))
        except Exception, e:
            xbmc.log(ADDONNAME + ': ' + str(e), xbmc.LOGERROR)
        return "", ""

    def readFile(self, filename):
        return open(filename).read()
