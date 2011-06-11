
class BaseModel( object ):

    def __init__(self, resource):
        self.resource = resource

    @classmethod
    def format( cls, data ):
        return cls.fmt % data
