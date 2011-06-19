#!/usr/bin/env python2
import pprint
import sys
import argparse
import os.path

from pkg_resources import resource_stream
from ConfigParser import RawConfigParser

from tiktok.lib.resources import init_resource
from tiktok import model
from tiktok import commands

CONFIG_FILE = '~/.tiktok/config.cfg'

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

    return config

def initialize( config ):

    modules = {
        'widget' : model.widget.Widget,
        'task' : model.task.Task,
    }

    for (mod, obj) in modules.items():
        obj.fmt = config[mod]['format']

    init_resource( config['url'], config['username'], config['password'] )


def dispatch( command, action, args ):

    module = vars( commands )[ command ]
    func = getattr( module, action )
    func( args )

def argparser():

    parser = argparse.ArgumentParser( 
            description = 'CLI app for interacting with TikTak.',
            prog='tiktok' 
            )

    parser.add_argument('-c', '--config', default = CONFIG_FILE , dest='configfile')
    parser.add_argument('-u', '--username', dest='username', default = argparse.SUPPRESS )
    parser.add_argument('-p', '--password', dest='password', default = argparse.SUPPRESS )
    parser.add_argument('--url', dest='url', default = argparse.SUPPRESS )

    commands = parser.add_subparsers(dest='command')

    #Tasks
    task_main = commands.add_parser(
            'task',
            #aliases = ['t', 'ta'],
            description = 'Task related commands'
            )

    task = task_main.add_subparsers(dest='action')

    show = task.add_parser(
            'show',
            description = 'Show detailed information about a task',
            #aliases = ['sh']
            )

    start = task.add_parser(
            'start',
            description = 'Start working on a task',
            #aliases = ['sta']
            )
    start.add_argument( 'tasknum', type = int )

    stop = task.add_parser(
            'stop',
            description = 'Stop working on current task',
            #aliases = ['sto']
            )
    stop.add_argument('-l', '--log', nargs = '+' )

    current = task.add_parser(
            'current',
            description = 'Information about the task you are working on right now',
            #aliases = ['cu']
            )

    #Widget
    widget_main = commands.add_parser(
            'widget',
            description = 'Widget commands',
            #aliases = ['wi']
            )
    widget = widget_main.add_subparsers(dest='action')

    tasks = widget.add_parser(
            'tasks',
            description = 'List of tasks inside a widget',
            #aliases = ['ta']
            )
    tasks.add_argument('widget_id', type = int )

    w_list = widget.add_parser(
            'list',
            description = 'List of available widgets',
            #aliases = ['li']
            )

    return parser

def error(message):
    print "ERROR: ", message
    argparser().parse_args(['--help'])
    sys.exit(1)

def main():

    parser = argparser()
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

if __name__ == '__main__':
    main()

