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

def search(msName):
    log(SCRIPTNAME," Move/Series Name %s " % msName , "NOTICE")
    


params = get_params()
#xbmc.log("Params %s" % params['action'], level=xbmc.LOGDEBUG)
log(SCRIPTNAME,"[%s] params" % params['action'])

if params['action'] == 'search':
    log(SCRIPTNAME, "Version %s"%VERSION,"NOTICE" )
    log(SCRIPTNAME, "Params [ %s ]" %params['action'],"NOTICE")

    movieSeriesHash   = {}
    if xbmc.Player().isPlaying():
        log( __name__, "action '%s' called" % params['action'],"NOTICE")
        movieSeriesHash = {}
        movieSeriesHash['temp']               = False
        movieSeriesHash['rar']                = False
        movieSeriesHash['mansearch']          = False
        movieSeriesHash['year']               = xbmc.getInfoLabel("VideoPlayer.Year")                         # Year
        movieSeriesHash['season']             = str(xbmc.getInfoLabel("VideoPlayer.Season"))                  # Season
        movieSeriesHash['episode']            = str(xbmc.getInfoLabel("VideoPlayer.Episode"))                 # Episode
        #movieSeriesHash['tvshow']             = normalizeString(xbmc.getInfoLabel("VideoPlayer.TVshowtitle"))  # Show
        #movieSeriesHash['title']              = normalizeString(xbmc.getInfoLabel("VideoPlayer.OriginalTitle"))# try to get original title
        movieSeriesHash['tvshow']             = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")  # Show
        movieSeriesHash['title']              = xbmc.getInfoLabel("VideoPlayer.OriginalTitle")# try to get original title
        movieSeriesHash['file_original_path'] = xbmc.Player().getPlayingFile().decode('utf-8')                 # Full path of a playing file
        movieSeriesHash['3let_language']      = [] #['scc','eng']
        movieSeriesHash['preferredlanguage'] = unicode(urllib.unquote(params.get('preferredlanguage', '')), 'utf-8')
        movieSeriesHash['preferredlanguage'] = xbmc.convertLanguage(movieSeriesHash['preferredlanguage'], xbmc.ISO_639_2)
    else:
        movieSeriesHash['temp'] = False
        movieSeriesHash['rar'] = False
        movieSeriesHash['year'] = ""
        movieSeriesHash['season'] = ""
        movieSeriesHash['episode'] = ""
        movieSeriesHash['tvshow'] = ""
        movieSeriesHash['title'] = ""
        movieSeriesHash['file_original_path'] = ""
        movieSeriesHash['3let_language'] = []
        movieSeriesHash['preferredlanguage'] = unicode(urllib.unquote(params.get('preferredlanguage', '')), 'utf-8')
        movieSeriesHash['preferredlanguage'] = xbmc.convertLanguage(movieSeriesHash['preferredlanguage'], xbmc.ISO_639_2)


    if 'searchstring' in params:
        movieSeriesHash['mansearch'] = True
        movieSeriesHash['mansearchstr'] = params['searchstring']

    if movieSeriesHash['title'] == "":
        if xbmc.Player().isPlaying():
            log("VideoPlayer.OriginalTitle not found")
            movieSeriesHash['title'] = normalizeString(xbmc.getInfoLabel("VideoPlayer.Title"))  # no original title, get just Title
        else:
            movieSeriesHash['title'] = "Search For..." # Needed to avoid showing previous search result.

    if params['action'] == 'manualsearch':
        if movieSeriesHash['season'] != '' or movieSeriesHash['episode']:
            movieSeriesHash['tvshow'] = params['searchstring']
        else:
            movieSeriesHash['title'] = params['searchstring']

    for lang in unicode(urllib.unquote(params['languages']), 'utf-8').split(","):
        movieSeriesHash['3let_language'].append(xbmc.convertLanguage(lang, xbmc.ISO_639_2))

    log("movieSeriesHash before cleaning: \n    %s" % movieSeriesHash)

    # clean title + tvshow params
    #clean_title(movieSeriesHash)
    #parse_rls_title(movieSeriesHash)

    if movieSeriesHash['episode'].lower().find("s") > -1:  # Check if season is "Special"
        movieSeriesHash['season'] = "0"
        movieSeriesHash['episode'] = movieSeriesHash['episode'][-1:]

    if movieSeriesHash['file_original_path'].find("http") > -1:
        movieSeriesHash['temp'] = True

    elif movieSeriesHash['file_original_path'].find("rar://") > -1:
        movieSeriesHash['rar'] = True
        movieSeriesHash['file_original_path'] = os.path.dirname(movieSeriesHash['file_original_path'][6:])

    elif movieSeriesHash['file_original_path'].find("stack://") > -1:
        stackPath = movieSeriesHash['file_original_path'].split(" , ")
        movieSeriesHash['file_original_path'] = stackPath[0][8:]
    log("%s" % movieSeriesHash)
    search(movieSeriesHash)

#elif params['action'] == 'manualsearch':
#    log(SCRIPTNAME, "Params [ %s ]" %params['action'],"NOTICE")

elif params['action'] == 'download':
    log(SCRIPTNAME, "Params [ %s ]" %params['action'],"NOTICE")

elif params['action'] == 'checkLogins':
    log(SCRIPTNAME, "Params [ %s ]" %params['action'],"NOTICE")
    superSub = subtitleEngine()
    superSub.checkLogins()



xbmcplugin.endOfDirectory(int(sys.argv[1]))