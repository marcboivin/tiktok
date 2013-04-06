from urlparse import urlparse

from tiktok.model.task import Task
from tiktok.model.url import URL

import pprint
import datetime
import sys


def live( args, helper ):
    pprint.pprint( 'You\'re going to live clock on a url' )
    
    url = urlparse( args['source_url'] )
    # Single subdomain implied. Also implied is that this subdomain 
    # identifies the parser to use
    system = url.hostname.split( '.' )[0]
    
    pprint.pprint( url )
    
    
def clock( args, helper ):
    pprint.pprint( 'You\'re goint to clock a past task' )
        