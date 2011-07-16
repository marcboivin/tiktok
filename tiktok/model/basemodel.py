from tiktok.lib.helpers import get_helper
from collections import namedtuple

def resourcemethod( func ):

    @classmethod
    def wrapper( cls, *args, **kwargs ):

        helpers = get_helper()

        Context = namedtuple('Context', ['resource', 'duration', 'datetime', 'task_properties'] )

        context = Context(
            helpers.resource,
            helpers.duration,
            helpers.datetime,
            helpers.config['task_properties']
        )

        if 'context' in kwargs:
            for key, value in kwargs['context'].items():
                setattr( context, key, value )

        return func( cls, context, *args, **kwargs )

    return wrapper

class BaseModel( dict ):

    def __init__(self, attributes, context, **kwargs ):

        dict.__init__( self )
        for key, value in context._asdict().items():
            setattr( self, key, value )
        self.update( attributes )
