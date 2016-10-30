# -*- coding: utf-8 -*-
#
#     Copyright (C) 2016 ScubaDiveTeam
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#


#import sys
#import urllib
#import shutil


#from requests import post

import codecs
import glob
#import os
import shutil
import sys
import time
import urllib
from os import path

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

# XBMC loglevel == -1 (NONE, nothing at all is logged)
# XBMC loglevel == 0 (NORMAL, shows LOGNOTICE, LOGERROR, LOGSEVERE and LOGFATAL) 
# XBMC loglevel == 1 (DEBUG, shows all)

ADDON       = xbmcaddon.Addon()
AUTHOR      = ADDON.getAddonInfo('author')
SCRIPTID    = ADDON.getAddonInfo('id')
SCRIPTNAME  = ADDON.getAddonInfo('name')
VERSION     = ADDON.getAddonInfo('version')
LANGUAGE    = ADDON.getLocalizedString

CWD         = unicode(xbmc.translatePath(ADDON.getAddonInfo('path')), 'utf-8')
PROFILE     = unicode(xbmc.translatePath(ADDON.getAddonInfo('profile')), 'utf-8')
RESOURCE    = unicode(xbmc.translatePath(path.join(CWD, 'resources', 'lib')), 'utf-8')
TEMP        = unicode(xbmc.translatePath(path.join(PROFILE, 'temp')), 'utf-8')

sys.path.append(RESOURCE)


from superSubtitleEngine import subtitleEngine, superSearchEngine
from subtitleUtils import log,notify, get_params
#from superSearchEngine import searchEngine, log 



params = get_params()
#xbmc.log("Params %s" % params['action'], level=xbmc.LOGDEBUG)
log(SCRIPTNAME,"[%s] params" % params['action'])
if params['action'] in ['search', 'manualsearch']:
    log(SCRIPTNAME, "Params [ %s ]" %params['action'],"NOTICE")
elif params['action'] == 'checkLogins':
    log(SCRIPTNAME, "Params [ %s ]" %params['action'],"NOTICE")
    superSub = subtitleEngine()
    superSub.checkLogins()

xbmcplugin.endOfDirectory(int(sys.argv[1]))