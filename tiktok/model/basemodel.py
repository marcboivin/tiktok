
resource = None

def get_resource():
    global resource
    return resource

def set_resource( new_resource ):
    global resource
    resource = new_resource

class BaseModel( object ):

    def __init__(self, resource=None):

        resource = resource or get_resource()
        if not resource:
            raise RuntimeError("resource is null and no default resource has been initialized")

        self.resource = resource

    @classmethod
    def format( cls, data ):
        return cls.fmt % data
