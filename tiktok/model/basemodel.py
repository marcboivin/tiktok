
resource = None

def get_resource():
    global resource
    return resource

def set_resource( new_resource ):
    global resource
    resource = new_resource

def resourcemethod( func ):

    @classmethod
    def wrapper( cls, *args, **kwargs ):
        resource = kwargs.get('resource', get_resource())

        return func( cls, resource, *args, **kwargs )

    return wrapper

class BaseModel( dict ):

    def __init__(self, attributes, resource=None):

        resource = resource or get_resource()
        if not resource:
            raise RuntimeError("resource is null and no default resource has been initialized")

        self.resource = resource
        self.update( attributes )

    def format( self ):
        return self.fmt % self
