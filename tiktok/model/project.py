from basemodel import resourcemethod
from cachemodel import CacheModel

class Project( CacheModel ):

    routes = {
        'list' : '/projects/list.json',
    }

    def __init__(self, *args, **kwargs ):

        CacheModel.__init__( self, *args, **kwargs )

    @resourcemethod
    def list( cls, **kwargs ):

        resource = kwargs['resource']
        data = resource.getjson( cls.routes['list'] )

        projects = [
            cls( p['project'], **kwargs ) for p in data
        ]

        cls.update_cache( projects, 'id', 'name' )

        return projects

    @resourcemethod
    def find_id_by_name( cls, name, **kwargs ):

        results = cls.search( name )

        if len( results ) == 0:
            cls.list()
            results = cls.search( name )

        if len( results ) > 1:
            raise ValueError("More than one project with the same name")

        return results[0][1]

