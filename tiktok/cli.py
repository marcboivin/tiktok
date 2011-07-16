#!/usr/bin/env python2
import pprint
import sys
import argparse
import os.path

from pkg_resources import resource_stream
from ConfigParser import RawConfigParser

from tiktok import model
from tiktok import commands

from lib.resources import TikTakResource
from lib.textdict import TextDict
from lib.argparser import argparser
from lib import durations, helpers

CONFIG_DIR = os.path.expanduser('~/.tiktok')

CONFIG_FILE = os.path.join( CONFIG_DIR, 'config.cfg' )
PROJECT_CACHE = os.path.join( CONFIG_DIR, 'projects.txt' )
USER_CACHE = os.path.join( CONFIG_DIR, 'users.txt' )

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

def initialize( config ):

    resource = TikTakResource( config['url'], config['username'], config['password'] )
    resource.login()

    helpers.set_helper( helpers.create_helper( config, resource ) )

    projects = TextDict( filename = PROJECT_CACHE )
    if os.path.exists( PROJECT_CACHE ):
        projects.load()

    users = TextDict( filename = USER_CACHE )
    if os.path.exists( USER_CACHE ):
        users.load()

    model.project.Project.cache = projects
    model.user.User.cache = users

def cleanup():

    model.project.Project.cache.save()
    model.user.User.cache.save()

def dispatch( command, action, args ):

    module = vars( commands )[ command ]
    func = getattr( module, action )
    func( args, helpers.get_helper() )

def error(message):
    print "ERROR: ", message
    argparser( CONFIG_FILE ).parse_args(['--help'])
    sys.exit(1)

def main():

    parser = argparser( CONFIG_FILE )
    args = vars( parser.parse_args() )

    command = args.pop('command')
    action = args.pop('action')
    configfile = os.path.expanduser( args.pop('configfile') )

    config = load_config( configfile )

    if not command:
        error("no command found")
    if not action:
        error("no action for command")

    required = ['url', 'username', 'password']
    for key in required:
        if key in args:
            config[key] = args.pop(key)

    missing = [x for x in required if not config.get(x) ]
    if len(missing) > 0:
        msg = "Missing arguments : %s\n" % ', '.join(missing)
        msg += "Please add them to the config file or pass them as arguments to the command line\n"
        error(msg)

    initialize( config )

    dispatch( command, action, args )

    cleanup()

if __name__ == '__main__':
    main()

