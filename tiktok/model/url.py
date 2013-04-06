import datetime
from basemodel import BaseModel

class URL( BaseModel ):
    __init__(self, *args, **kwargs ):
        BaseModel.__init__( self, *args, **kwargs )
        
    def select_system( self, url ):
        return False
        
    def fetch_content( self ):
        return False
        
    def clock( self, date, start_time, stop_time )