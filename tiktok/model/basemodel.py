import datetime
import time

from tiktok.lib.durations import total_seconds

utils = {}

def get_utils():
    global utils
    return utils

def set_utils( new_utils ):
    global utils
    utils = new_utils

utc_datetime = '%Y-%m-%dT%H:%M:%SZ'

def parse_isoutc( text ):

    dt = datetime.datetime.strptime( text, utc_datetime )
    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
    secs = total_seconds( dt - epoch )
    return datetime.datetime.utcfromtimestamp( secs )

def resourcemethod( func ):

    @classmethod
    def wrapper( cls, *args, **kwargs ):
        new_kw = get_utils()
        new_kw.update( kwargs )
        return func( cls, *args, **new_kw )

    return wrapper

class BaseModel( dict ):

    def __init__(self, attributes, **kwargs ):

        dict.__init__( self )
        for key, value in kwargs.items():
            setattr( self, key, value )
        self.update( attributes )
