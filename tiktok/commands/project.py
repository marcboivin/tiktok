import pprint

from tiktok.model.project import Project

def list( args, config, **kwargs ):

    pprint.pprint( Project.list() )
