from cachemodel import CacheModel
from basemodel import resourcemethod

class User( CacheModel ):

    routes = {
        'list' : '/users/list.json',
    }

    def __init__( self, *args, **kwargs ):
        CacheModel.__init__( self, *args, **kwargs )

    @resourcemethod
    def list( cls, context ):
        resource = context.resource

        data = resource.getjson( cls.routes['list'] )

        users = [
            cls( u['user'], context ) for u in data
        ]

        cls.update_cache( users, 'id', 'username' )

        return users

    @resourcemethod
    def find_id_by_username( cls, context, username ):

        results = cls.search( username )

        if len( results ) == 0:
            cls.list()
            results = cls.search( username )

        return [ r[0] for r in results ]
