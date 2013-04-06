import os.path

from pkg_resources import resource_stream
from ConfigParser import RawConfigParser

configs = False

CONFIG_DIR = os.path.expanduser('~/.tiktok')

CONFIG_FILE = os.path.join( CONFIG_DIR, 'config.cfg' )

def load_config( path ):
    config = {}
    
    defaults = resource_stream('tiktok.config', 'defaults.cfg')
    parser = RawConfigParser(allow_no_value = True)
    parser.readfp( defaults, 'defaults.cfg' )
    
    if os.path.exists( path ):
        parser.read( path )

    sections = [ x for x in parser.sections() if x != 'general' ]

    config.update( dict( parser.items('general') ) )
    for section in sections:
        config[section] = dict( parser.items( section ) )

    config['config_dir'] = CONFIG_DIR

    task_properties = zip(
        [ int( x ) for x in config['task']['property_ids'].split(',') ],
        [ int( x ) for x in config['task']['property_values'].split(',') ]
    )

    config['task_properties'] = task_properties

    return config