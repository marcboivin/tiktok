from urlparse import urlparse

from tiktok.model.task import Task
from tiktok.model.url import URL

import pprint
import datetime
import sys


def live( args, helper ):
    pprint.pprint( 'You\'re going to live clock on a url' )
    
    url = URL( args['source_url'] )
    url.live( )
    
    
def clock( args, helper ):
    pprint.pprint( 'You\'re goint to clock a past task NOT IMPLEMENTED YET' )
    url = urlparse( args['source_url'] )
    url.clock( )    