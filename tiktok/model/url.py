import datetime
from urlparse import urlparse

from tiktok.model import Task
from tiktok.lib import resources, config

class URL( object ):
    def __init__(self, url, *args, **kwargs ):
        
        url = urlparse( url )
        
        self.url = url
        self.select_ressource( )
        self.init_ressource( )
        
    def clock( self, date, start_time, stop_time ):
        return False
        
    def live( self ):
        taskname = self.ressource.get_task_name( )
        projet = self.ressource.get_project_id( )

        return False
        
    def select_ressource( self ):
        '''
            Which ressrouce do you need. Probably could be a factory
            pattern.

            Single subdomain implied. Also implied is that this subdomain 
            identifies the Ressource to use
        '''
        system = self.url.hostname.split( '.' )[0]

        # Build the ressource name based on the system name
        self.selected_ressource =  vars( resources )[ system.capitalize() + 'Ressource' ]
    
    def init_ressource( self ):
        path = self.url.path.split( '/' )
        ID = path[len( path ) - 1]

        self.ressource = self.selected_ressource( self.url.hostname, self.url.scheme, config.configs['username'], config.configs['password'], ID )


        