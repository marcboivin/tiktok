import pprint

from tiktok.model.user import User

def list( args, config, **kwargs ):

    pprint.pprint( User.list() )
