
utils = {}

def get_utils():
    global utils
    return utils

def set_utils( new_utils ):
    global utils
    utils = new_utils

def resourcemethod( func ):

    @classmethod
    def wrapper( cls, *args, **kwargs ):
        new_kw = get_utils()
        new_kw.update( kwargs )
        return func( cls, *args, **new_kw )

    return wrapper

class BaseModel( dict ):

    def __init__(self, attributes, **kwargs ):

        self.resource = kwargs['resource']
        self.duration_parser = kwargs['duration_parser']
        self.update( attributes )
