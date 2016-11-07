import cookielib
import datetime
import re
import urllib
import urllib2
import zlib
import json

import bs4

import xbmc
from lib.subtitleUtils import log, notify


class subtitleLibrary(object):

    def __init__(self):
        self.global_name = ""

class webCheckLogins(object):
    BASE_URLS = { 
        'subcenterUrl' : 'http://www.subscenter.org/%s/api/',
        'torecUrl'     : 'http://www.torec.net/login.asp'  
        }
    SITE_AUTH_STRACTURE = {
            'torec' : 
                {
                    "ref": "/Default.asp?",
                    "Form": "True",
                    "site": "true",
                    "username": %s,
                    "password": %s,
                    "login": "submit"
                },
            'subcenterUrl' : {
                
            }
     }

    def __init__(self, sites=None ):
        self.siteToCheck = sites
    
    def _checkAuthentication(self):
        
        self.siteToCheck = sites
