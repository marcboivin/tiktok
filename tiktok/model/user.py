from cachemodel import CacheModel
from basemodel import resourcemethod

class User( CacheModel ):

    routes = {
        'list' : '/users/list.json',
    }

    def __init__( self, *args, **kwargs ):
        CacheModel.__init__( self, *args, **kwargs )

    @resourcemethod
    def list( cls, **kwargs ):
        resource = kwargs['resource']

        data = resource.getjson( cls.routes['list'] )

        users = [
            cls( u['user'], **kwargs ) for u in data
        ]

        cls.update_cache( users, 'id', 'username' )

        return users

    @resourcemethod
    def find_id_by_username( cls, username, **kwargs ):

        results = cls.search( username )

        if len( results ) == 0:
            cls.list()
            results = cls.search( name )

        if len( results ) > 1:
            raise ValueError("More than one user with the same username")

        return results[0][1]
