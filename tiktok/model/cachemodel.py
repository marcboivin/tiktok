from basemodel import BaseModel

class CacheModel( BaseModel ):

    @classmethod
    def update_cache( cls, elements, key, value ):

        if not hasattr( cls, 'cache' ):
            cls.cache = {}

        cls.cache.update( dict (
            ( e[key], e[value] ) for e in elements
        ) )

        return cls.cache

    @classmethod
    def search( cls, term ):

        if not hasattr( cls, 'cache' ):
            return []

        term = term.lower()
        elements = dict( ( key, value.lower() ) for ( key, value ) in cls.cache.items() )
        found = [ ( key, cls.cache[key] ) for (key, value) in elements.items() if value.find( term ) > -1 ]
        return found

