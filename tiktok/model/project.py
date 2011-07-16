from basemodel import resourcemethod
from cachemodel import CacheModel

class Project( CacheModel ):

    routes = {
        'list' : '/projects/list.json',
    }

    def __init__(self, *args, **kwargs ):

        CacheModel.__init__( self, *args, **kwargs )

    @resourcemethod
    def list( cls, context ):

        resource = context.resource
        data = resource.getjson( cls.routes['list'] )

        projects = [
            cls( p['project'], context ) for p in data
        ]

        cls.update_cache( projects, 'id', 'name' )

        return projects

    @resourcemethod
    def find_id_by_name( cls, context, name ):

        results = cls.search( name )

        if len( results ) == 0:
            cls.list()
            results = cls.search( name )

        return [ r[0] for r in results ]

