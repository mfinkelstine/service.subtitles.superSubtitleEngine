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