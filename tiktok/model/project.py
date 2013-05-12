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
        # list.json is paginated since we can't know how many 
        # pages there are, here's - yet another - dirty hack
        i = 1
        projects = []
        while i < 5:
            data = resource.getjson( cls.routes['list'], {}, {}, {'page':i} )

            projects += [
                cls( p['project'], context ) for p in data
            ]

            i += 1

        cls.update_cache( projects, 'id', 'name' )


        return projects

    @resourcemethod
    def find_id_by_name( cls, context, name ):

        results = cls.search( name )

        if len( results ) == 0:
            cls.list()
            results = cls.search( name )

        return [ r[0] for r in results ]

